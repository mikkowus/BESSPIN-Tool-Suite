"""
Project: SSITH CyberPhysical Demonstrator
director.py
Author: Ethan Lew <elew@galois.com>
Date: 04/05/2021
Python 3.8.3
O/S: Windows 10

Interface to manage ignition components
"""
import cyberphyslib.demonstrator.can as ccan
import cyberphyslib.demonstrator.simulator as simulator
import cyberphyslib.demonstrator.speedometer as speedo
import cyberphyslib.demonstrator.leds_manage as ledm
import cyberphyslib.demonstrator.infotainment as infotain
import cyberphyslib.demonstrator.config as cconf
import cyberphyslib.canlib as canlib

from cyberphyslib.demonstrator.handler import ComponentHandler
from cyberphyslib.demonstrator.logger import ignition_logger

#import transitions
from transitions.extensions import GraphMachine as Machine
from transitions import State

import time


class IgnitionDirector:
    """
    Ignition program that implements the desired execution flow

    IgnitionDirector is a Moore FSM with 9 states and 6 inputs, namely

        input = {component_fail, fadecandy_fail, scenario_timeout, cc_msg, can_msg, self_drive}
        state = {startup, noncrit_failure, ready, terminate, self_drive, restart, timeout, cc_msg, can}

    Two states whose transitions depend on input are startup and the ready state.
    """
    # FSM description
    states=[State(name='startup', on_enter='startup_enter'),
            State(name='noncrit_failure', on_enter='noncrit_failure_enter'),
            State(name='ready', on_enter='ready_enter'),
            State(name='terminate', on_enter='terminate_enter'),
            State(name='self_drive', on_enter='self_drive_enter'),
            State(name='restart', on_enter='restart_enter'),
            State(name='timeout', on_enter='timeout_enter'),
            State(name='cc_msg', on_enter='cc_msg_enter'),
            State(name='can', on_enter='can_enter')]

    transitions = [
        # startup logic
        { 'trigger': 'next_state', 'source': 'startup', 'dest': 'noncrit_failure',
          'conditions': 'input_fadecandy_fail', 'unless': 'input_component_fail'},
        { 'trigger': 'next_state', 'source': 'startup', 'dest': 'terminate',
          'conditions': 'input_component_fail' },
        { 'trigger': 'next_state', 'source': 'startup', 'dest': 'ready',
          'unless': ['input_component_fail', 'input_fadecandy_fail'] },
        { 'trigger': 'next_state', 'source': 'noncrit_failure', 'dest': 'ready'},

        # ready logic
        {'trigger': 'next_state', 'source': 'ready', 'dest': 'ready',
         'unless': ['input_s_timeout', 'input_cc_msg', 'input_can_msg', 'input_self_drive']},
        {'trigger': 'next_state', 'source': 'ready', 'dest': 'self_drive',
         'conditions': 'input_self_drive', 'unless': ['input_cc_msg', 'input_can_msg', 'input_s_timeout']},
        {'trigger': 'next_state', 'source': 'ready', 'dest': 'timeout',
         'conditions': 'input_s_timeout'},
        {'trigger': 'next_state', 'source': 'ready', 'dest': 'cc_msg',
         'conditions': 'input_cc_msg', 'unless': 'input_s_timeout'},
        {'trigger': 'next_state', 'source': 'ready', 'dest': 'can',
         'conditions': 'input_can_msg', 'unless': ['input_cc_msg', 'input_s_timeout']},

        {'trigger': 'next_state', 'source': 'timeout', 'dest': 'restart'},
        {'trigger': 'next_state', 'source': 'restart', 'dest': 'ready'},
        #{'trigger': 'next_state', 'source': 'restart', 'dest': 'terminate'},
        {'trigger': 'next_state', 'source': 'can', 'dest': 'ready'},
        {'trigger': 'next_state', 'source': 'self_drive', 'dest': 'restart'},
        {'trigger': 'next_state', 'source': 'cc_msg', 'dest': 'ready'},
        {'trigger': 'next_state', 'source': 'cc_msg', 'dest': 'restart'}
    ]

    def __init__(self):
        self.can_multiverse = None
        self.info_net = None
        self.proxy = None

        # TODO: FIXME: these aren't realistic values
        # NOTE: there are inconsistencies between TcpBus and UdpBus arguments
        self.cc_ip_addr = "127.0.0.1:5030"
        self.cc_subscribers = ["127.0.0.1:5030"]
        self.scenario_timeout = 3 * 60 # (s) 3 minutes
        self.cc_timeout = 20 # 20 seconds

        self._handler = ComponentHandler()
        self.machine = Machine(self, states=self.states, transitions=self.transitions, initial='startup', show_conditions=True)

        self.input_fadecandy_fail = False
        self.input_component_fail = False
        self.input_can_msg = False
        self.input_cc_msg = False
        self.input_s_timeout = False
        self.input_self_drive = False
        #self.startup_enter()

    def run(self):
        self.startup_enter()
        while True:
            self.next_state()

    def default_input(self):
        self.input_fadecandy_fail = False
        self.input_component_fail = False
        self.input_can_msg = False
        self.input_cc_msg = False
        self.input_s_timeout = False
        self.input_self_drive = False

    def terminate_enter(self):
        ignition_logger.debug("Termination State: Enter")
        self._handler.exit()

    def noncrit_failure_enter(self):
        ignition_logger.debug("Noncritical Failure State: Enter")

    def startup_enter(self):
        def register_components():
            # register call of the components to the CAN multiverse network
            for c in self._handler.components:
                if c.name != "canm":
                    self.can_multiverse.register(c)

        ignition_logger.debug("Startup State: Enter")
        simulator.Sim.kill_beamng(1)

        sip = cconf.SIM_IP
        can_ssith_info = ccan.CanUdpNetwork("secure_infotainment", cconf.CAN_PORT, sip)
        can_ssith_ecu = ccan.CanUdpNetwork("secure_ecu", cconf.CAN_PORT, sip)
        can_base = ccan.CanUdpNetwork("base", cconf.CAN_PORT, sip)
        networks = [can_base, can_ssith_ecu, can_ssith_info]

        # TODO: FIXME
        # can_ssith_info.whitelist = cconf.SSITH_INFO_WHITELIST
        # can_ssith_ecu.whitelist = cconf.SSITH_ECU_WHITELIST
        # can_base.whitelist = cconf.BASE_WHITELIST
        # can_ssith_info.blacklist = cconf.SSITH_INFO_BLACKLIST
        # can_ssith_ecu.blacklist = cconf.SSITH_ECU_BLACKLIST
        # can_base.blacklist = cconf.BASE_BLACKLIST

        # start the can networks
        self.cc_bus = canlib.TcpBus(self.cc_ip_addr, self.cc_subscribers)
        self.can_multiverse = ccan.CanMultiverse("multiverse", networks, default_network="base")
        self.info_net = ccan.CanUdpNetwork("info-net", cconf.INFO_UI_PORT, sip)

        # startup beamng
        msg = self._handler.start_component(simulator.Sim())
        if msg != simulator.BeamNgStatus.READY:
            ignition_logger.debug(f"BeamNG Sim service failed to start ({msg})")
            self.input_fadecandy_fail = False
            self.input_component_fail = True
            return

        # startup the multiverse
        msg = self._handler.start_component(ccan.CanMultiverseComponent(self.can_multiverse))
        if msg != ccan.CanMultiverseStatus.READY:
            ignition_logger.debug(f"CAN multiverse service failed to start ({msg})")
            self.input_fadecandy_fail = False
            self.input_component_fail = True
            return

        # startup infotainment proxy
        self.proxy = infotain.InfotainmentProxy(self.info_net, self.can_multiverse)
        self._handler.start_component(self.proxy.info_ui, wait=False)
        self._handler.start_component(self.proxy.info_player, wait=False)

        # startup the speedometer
        msg = self._handler.start_component(speedo.Speedo())
        if msg != speedo.SpeedoStatus.READY:
            ignition_logger.debug(f"Speedometer service failed to start ({msg})")
            self.input_fadecandy_fail = False
            self.input_component_fail = True
            return

        # startup led manager
        msg = self._handler.start_component(ledm.LedManagerComponent.for_ignition())
        if msg != ledm.LedManagerStatus.READY:
            ignition_logger.debug(f"LED Manager service failed to start ({msg})")
            register_components()
            self.input_fadecandy_fail = True
            self.input_component_fail = False
            return

        # add everything to the can multiverse network
        register_components()

        self.input_fadecandy_fail = False
        self.input_component_fail = False
        return

    def ready_enter(self):
        ignition_logger.debug("Ready state: enter")
        scenario_start = time.time()
        while((time.time() - scenario_start) < self.scenario_timeout):
            cc_recv = self.cc_bus.recv(timeout=self.cc_timeout)
            if cc_recv:
                self.default_input()
                self.input_cc_msg = True
                # process the cc_packet
                pass
            else:
                self.default_input()
                self.input_self_drive = True
                #self.ready_self_drive()
                return

        self.default_input()
        self.input_s_timeout = True

    def restart_enter(self, n_resets=3):
        ignition_logger.debug("Restart state: enter")
        msg = self._handler.message_component("beamng", simulator.BeamNgCommand.RESTART, do_receive=True)
        if msg != simulator.BeamNgStatus.RESTART_FINISHED:
            ignition_logger.warning(f"BeamNG restart failed ({n_resets})!")
            if n_resets >= 0:
                self.restart_enter(n_resets=n_resets - 1)
            else:
                ignition_logger.warning(f"BeamNG restart failed! Terminating...")
                return
        self.default_input()

    def noncrit_failure_enter(self):
        ignition_logger.debug("Noncrit_failure state: enter")
        ignition_logger.error("Ignition achieved a noncritical error. The LED manager failed to start. Continuing anyway...")
        self.default_input()
        return

    def self_drive_enter(self):
        msg = self._handler.message_component("beamng", simulator.BeamNgCommand.ENABLE_AUTOPILOT, do_receive=True)
        # TODO: FIXME: conditions to disable autopilot
        time.sleep(20.0)
        msg = self._handler.message_component("beamng", simulator.BeamNgCommand.DISABLE_AUTOPILOT, do_receive=True)
        self.default_input()

    def timeout_enter(self):
        ignition_logger.info("Timeout state: enter")
        self.default_input()

    def draw_graph(self, fname: str):
        """draw a fsm graphviz graph (for documentation, troubleshooting)

        NOTE: you will need to install graphviz (with dot)
        """
        self.machine.get_graph().draw(fname, prog='dot')


if __name__ == "__main__":
    fsm = IgnitionDirector()
    fsm.draw_graph('state_diagram.png')