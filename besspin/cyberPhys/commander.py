#! /usr/bin/env python3

from besspin.base.utils.misc import *
import besspin.cyberPhys.launch
import besspin.cyberPhys.cyberphyslib.cyberphyslib.demonstrator.component as ccomp
import besspin.cyberPhys.cyberphyslib.cyberphyslib.canlib as canlib

import time
import struct
import can as extcan
from enum import Enum, auto

class CommanderStates(Enum):
    '''
    FSM description
    '''
    BOOT = auto() # All targets booted OK
    READY = auto() # Targets are ready
    RESTART_TARGET = auto() # Restart target
    FAILIURE_RECOVERY = auto() # Attempt to recovery a failed restart
    DEGRADED_MODE = auto() # Initialize degraded mode
    TERMINATE = auto() # Terminate the tool

class Commander(ccomp.ComponentPoller):
    """
    Cyberphys commander
    """
    READY_MSG_TIMEOUT = 10.0 #[s]
    CC_TIMEOUT = 0.1
    POLL_FREQ = 1.0
    DEBUG = True

    target_ids = {
        canlib.TEENSY: 0,
        canlib.TARGET_1: 1,
        canlib.TARGET_2: 2,
        canlib.TARGET_3: 3,
        canlib.TARGET_4: 4,
        canlib.TARGET_5: 5,
        canlib.TARGET_6: 6,
    }

    target_list = [k for k in target_ids.keys()]

    def __init__(self):
        # Communication with other components
        name = "commander"
        in_socks, out_socks = besspin.cyberPhys.launch.getComponentPorts(name)
        super().__init__(name, in_socks, out_socks, sample_frequency=self.POLL_FREQ)

        self.state = CommanderStates.BOOT

        # input space as class members
        self.target_reset_requested = False
        self.ready_msg_timeout = False
        self.target_error = False
        self.restart_ok = False
        self.recovery_possible = False
        self.restart_failed = False
        self.degraded_mode_possible = False
        self.targets = ["READY"] * (getSetting('nTargets')+1) # To account for teensy
        self.last_ready_msg = 0.0

        # C&C Network connection
        host, subscribers = besspin.cyberPhys.launch.getNetworkNodes("AdminPc")
        self.cc_bus = canlib.TcpBus(host, subscribers)

        self.start_poller()

    def on_poll_poll(self, t):
        """main loop"""
        # NOTE: You may want to check for termination so that you don't need to add a cycle at terminate.

        if self.state == CommanderStates.BOOT:
            #     # startup logic
            #     { 'trigger': 'next_state', 'source': 'boot', 'dest': 'ready'},
            # Finish booting
            printAndLog(f"<{self.__class__.__name__}> booted.", doPrint=Commander.DEBUG)
            self.state = CommanderStates.READY
        elif self.state == CommanderStates.READY:
            # Most common state
            #     # ready logic
            #     {'trigger': 'next_state', 'source': 'ready', 'dest': 'ready',
            #      'unless': ['target_error, target_reset_requested']},
            self.ready_enter()
            if self.target_reset_requested:
            #     {'trigger': 'next_state', 'source': 'ready', 'dest': 'restart_target',
            #      'conditions': 'target_reset_requested'},
                printAndLog(f"<{self.__class__.__name__}> Target restart requested", doPrint=Commander.DEBUG)
                self.state = CommanderStates.RESTART_TARGET
            elif self.target_error:
            #     {'trigger': 'next_state', 'source': 'ready', 'dest': 'restart_target',
            #      'conditions': 'target_error'},
                printAndLog(f"<{self.__class__.__name__}> Target error detected", doPrint=Commander.DEBUG)
                self.state = CommanderStates.RESTART_TARGET

        elif self.state == CommanderStates.RESTART_TARGET:
            # Attempt target restart
            if self.target_reset_requested:
                self.restart_target_enter()
                # TODO
                self.state = CommanderStates.READY
            elif self.restart_ok:
                #     {'trigger': 'next_state', 'source': 'restart_target', 'dest': 'ready',
                #      'conditions': 'restart_ok'},
                self.state = CommanderStates.READY
            else:
                printAndLog(f"<{self.__class__.__name__}> Waiting for target to become ready", doPrint=Commander.DEBUG)
                #     {'trigger': 'next_state', 'source': 'restart_target', 'dest': 'failure_recovery',
                #      'conditions': 'restart_failed'},
        elif self.state == CommanderStates.FAILIURE_RECOVERY:
            #     # recovery logic
            #     {'trigger': 'next_state', 'source': 'failure_recovery', 'dest': 'terminate',
            #      'unless': 'recovery_possible'},
            self.failure_recovery_enter()
        elif self.state == CommanderStates.DEGRADED_MODE:
            #     {'trigger': 'next_state', 'source': 'failure_recovery', 'dest': 'degraded_mode',
            #      'conditions': 'recovery_possible'},
            #     {'trigger': 'next_state', 'source': 'degraded_mode', 'dest': 'ready',
            #      'conditions': 'degraded_mode_possible'},
            logAndExit(f"<{self.__class__.__name__}> State not implemented")
        elif self.state == CommanderStates.TERMINATE:
            #     {'trigger': 'next_state', 'source': 'degraded_mode', 'dest': 'terminate',
            #      'unless': 'degraded_mode_possible'},
            self.terminate_enter()

    # TODO: handle sending component_id|error_code as required in message specs
    # TODO: add `dlc` into canspecs.py
    def send_component_error(self, component_id):
        msg = extcan.Message(arbitration_id=canlib.CAN_ID_CMD_COMPONENT_ERROR,
            dlc=8,
            data=struct.pack(canlib.CAN_FORMAT_CMD_COMPONENT_ERROR, component_id, 0))
        printAndLog(f"Commander sending {msg}",doPrint=True)
        self.cc_bus.send(msg)

    def send_component_ready(self, component_id):
        msg = extcan.Message(arbitration_id=canlib.CAN_ID_CMD_COMPONENT_READY,
            dlc=4,
            data=struct.pack(canlib.CAN_FORMAT_CMD_COMPONENT_READY, component_id))
        #printAndLog(f"Commander sending {msg}",doPrint=False)
        self.cc_bus.send(msg)

    def process_cc(self, msg):
        """process cc message
        """
        cid, data = msg.arbitration_id, msg.data

        try:
            if cid == canlib.CAN_ID_CMD_RESTART:
                dev_id = struct.unpack(canlib.CAN_FORMAT_CMD_RESTART, data)[0]
                printAndLog(f"<{self.__class__.__name__}> dev_id: {dev_id}", doPrint=Commander.DEBUG)
                if dev_id in self.target_ids:
                    targetId = self.target_ids[dev_id]
                    printAndLog(f"<{self.__class__.__name__}> targetId: {targetId}", doPrint=Commander.DEBUG)
                    self.targets[targetId] = "RESET"
                    self.target_reset_requested = True
                    
        except Exception as exc:
            printAndLog(f"<{self.__class__.__name__}> Error processing message: {msg}: {exc}")

    def ready_enter(self):
        """
        Most common state
        Check if there is a problem from the watchdog (target restarted)
        TODO: when to reset ALL targets?
        """
        # Periodically send CMD_COMPONENT_READY()
        if (time.time() - self.last_ready_msg) > self.READY_MSG_TIMEOUT:
            self.send_component_ready(canlib.BESSPIN_TOOL)
        
        # Check if there is a C&C restart request (single target)
        cc_recv = self.cc_bus.recv(timeout=self.CC_TIMEOUT)
        if cc_recv:
            print(cc_recv)
            self.process_cc(cc_recv)
    
    def restart_target_enter(self):
        """
        Initiate target restart
        """
        printAndLog(f"<{self.__class__.__name__}> Restarting target")
        self.target_reset_requested = False

        for targetId in range(1,getSetting('nTargets')+1):
            if self.targets[targetId] == "RESET":
                # Initiate reset of this target
                self.send_message(ccomp.Message(f"RESET {targetId}"), getSetting('cyberPhysComponentBaseTopic'))
                self.targets[targetId] = "WAIT"

    def failure_recovery_enter(self):
        """
        Not much to do here right now
        TODO: better failure recovery
        """
        printAndLog(f"<{self.__class__.__name__}> Attempting failure recovery...")

    def terminate_enter(self):
        """
        Send CMD_COMPONENT_ERROR before exiting
        NOTE: not sure how well this will fit the flow - maybe replace this
        with a call in __del__ function
        """
        self.send_component_error(canlib.BESSPIN_TOOL)
        printAndLog(f"<{self.__class__.__name__}> Terminating...")

    @recv_topic("base-topic")
    def _(self, msg, t):
        """Filter received messages"""
        printAndLog(f"<{self.__class__.__name__}> Received msg: {msg}",doPrint=False)
        for targetId in range(1,getSetting('nTargets')+1):
            if msg == f"READY {targetId}":
                self.targets[targetId] = "READY"
                self.restart_ok = True
                self.send_component_ready(self.target_list[targetId])
            elif msg == f"ERROR {targetId}":
                # Request a reset of the target
                self.targets[targetId] = "RESET"
                self.target_reset_requested = True
