"""Cyberphys Component IDs
Project: SSITH CyberPhysical Demonstrator
Name: ../cyberphyslib/cyberphyslib/canlib/componentids.py
Author: Steven Osborn <steven@lolsborn.com>, Kristofer Dobelstein, Ethan Lew <elew@galois.com>
Michal Podhradsky <mpodhradsky@galois.com>
Date: 20 August 2021
This file was created by BESSPIN-Tool-Suite/besspin/cyberPhys/canlib/make_can_spec.py
"""

SCENARIO_BASELINE = 0x11
SCENARIO_SECURE_INFOTAINMENT = 0x12
SCENARIO_SECURE_ECU = 0x13
FUNCTIONALITY_MINIMAL = 0x16
FUNCTIONALITY_MEDIUM = 0x17
FUNCTIONALITY_FULL = 0x18
BESSPIN_TOOL = 0x20
TARGET_1 = 0x21 # FreeRTOS_1
TARGET_2 = 0x22 # FreeRTOS_2(CHERI)
TARGET_3 = 0x23 # FreeRTOS_3
TARGET_4 = 0x24 # Debian_1
TARGET_5 = 0x25 # Debian_2(LMCO)
TARGET_6 = 0x26 # Debian_3
TEENSY = 0x27
IGNITION = 0x30
LED_COMPONENT = 0x31
HACKER_KIOSK = 0x40
HACK_NONE = 0x50
HACK_OTA = 0x51
HACK_BRAKE = 0x51
HACK_THROTTLE = 0x52
HACK_TRANSMISSION = 0x53
HACK_LKAS = 0x54
HACK_INFOTAINMENT_1 = 0x55
HACK_INFOTAINMENT_2 = 0x56
INFOTAINMENT_THIN_CLIENT = 0x60
INFOTAINMENT_SERVER_1 = 0x61
INFOTAINMENT_SERVER_2 = 0x62
INFOTAINMENT_SERVER_3 = 0x63
OTA_UPDATE_SERVER_1 = 0x64
OTA_UPDATE_SERVER_2 = 0x65
OTA_UPDATE_SERVER_3 = 0x66
BUTTON_STATION_1 = 0x01
BUTTON_STATION_2 = 0x02
BUTTON_STATION_3 = 0x03
BUTTON_VOLUME_DOWN = 0x10
BUTTON_VOLUME_UP = 0x11
SENSOR_THROTTLE = 0xBE
SENSOR_BRAKE = 0xBF
ERROR_UNSPECIFIED = 0xF0
