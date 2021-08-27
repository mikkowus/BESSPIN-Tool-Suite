"""Cyberphys Component IDs
Project: SSITH CyberPhysical Demonstrator
Name: ../cyberphyslib/cyberphyslib/canlib/componentids.py
Author: Steven Osborn <steven@lolsborn.com>, Kristofer Dobelstein, Ethan Lew <elew@galois.com>
Michal Podhradsky <mpodhradsky@galois.com>
Date: 26 August 2021
This file was created by BESSPIN-Tool-Suite/besspin/cyberPhys/canlib/make_can_spec.py
"""

SCENARIO_BASELINE = 0x11
SCENARIO_SECURE_INFOTAINMENT = 0x12
SCENARIO_SECURE_ECU = 0x13
FUNCTIONALITY_MINIMAL = 0x16
FUNCTIONALITY_MEDIUM = 0x17
FUNCTIONALITY_FULL = 0x18
BESSPIN_TOOL_FREERTOS = 0x20
FREERTOS_1 = 0x21
FREERTOS_2_CHERI = 0x22
FREERTOS_3 = 0x23
DEBIAN_1 = 0x24
DEBIAN_2_LMCO = 0x25
DEBIAN_3 = 0x26
TEENSY = 0x27
BESSPIN_TOOL_DEBIAN = 0x28
IGNITION = 0x30
LED_COMPONENT = 0x31
CAN_DISPLAY = 0x32
HACKER_KIOSK = 0x40
HACK_NONE = 0x50
HACK_OTA = 0x51
HACK_BRAKE = 0x51
HACK_THROTTLE = 0x52
HACK_TRANSMISSION = 0x53
HACK_LKAS = 0x54
HACK_INFOTAINMENT_VOLUME = 0x55 # Hacks info volume
HACK_INFOTAINMENT_MUSIC = 0x56 # Hacks info music
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
SENSOR_THROTTLE = 0xBE # Throttle sensor error (From FreeRTOS ECU)
SENSOR_BRAKE = 0xBF # Brake sensor error (From FreeRTOS ECU)
ERROR_UNSPECIFIED = 0xF0 # General error
ERROR_NONE = 0xFF # No error (clears errors)

CanlibComponentNames = {
	SCENARIO_BASELINE: "SCENARIO_BASELINE",
	SCENARIO_SECURE_INFOTAINMENT: "SCENARIO_SECURE_INFOTAINMENT",
	SCENARIO_SECURE_ECU: "SCENARIO_SECURE_ECU",
	FUNCTIONALITY_MINIMAL: "FUNCTIONALITY_MINIMAL",
	FUNCTIONALITY_MEDIUM: "FUNCTIONALITY_MEDIUM",
	FUNCTIONALITY_FULL: "FUNCTIONALITY_FULL",
	BESSPIN_TOOL_FREERTOS: "BESSPIN_TOOL_FREERTOS",
	FREERTOS_1: "FREERTOS_1",
	FREERTOS_2_CHERI: "FREERTOS_2_CHERI",
	FREERTOS_3: "FREERTOS_3",
	DEBIAN_1: "DEBIAN_1",
	DEBIAN_2_LMCO: "DEBIAN_2_LMCO",
	DEBIAN_3: "DEBIAN_3",
	TEENSY: "TEENSY",
	BESSPIN_TOOL_DEBIAN: "BESSPIN_TOOL_DEBIAN",
	IGNITION: "IGNITION",
	LED_COMPONENT: "LED_COMPONENT",
	CAN_DISPLAY: "CAN_DISPLAY",
	HACKER_KIOSK: "HACKER_KIOSK",
	HACK_NONE: "HACK_NONE",
	HACK_OTA: "HACK_OTA",
	HACK_BRAKE: "HACK_BRAKE",
	HACK_THROTTLE: "HACK_THROTTLE",
	HACK_TRANSMISSION: "HACK_TRANSMISSION",
	HACK_LKAS: "HACK_LKAS",
	HACK_INFOTAINMENT_VOLUME: "HACK_INFOTAINMENT_VOLUME",
	HACK_INFOTAINMENT_MUSIC: "HACK_INFOTAINMENT_MUSIC",
	INFOTAINMENT_THIN_CLIENT: "INFOTAINMENT_THIN_CLIENT",
	INFOTAINMENT_SERVER_1: "INFOTAINMENT_SERVER_1",
	INFOTAINMENT_SERVER_2: "INFOTAINMENT_SERVER_2",
	INFOTAINMENT_SERVER_3: "INFOTAINMENT_SERVER_3",
	OTA_UPDATE_SERVER_1: "OTA_UPDATE_SERVER_1",
	OTA_UPDATE_SERVER_2: "OTA_UPDATE_SERVER_2",
	OTA_UPDATE_SERVER_3: "OTA_UPDATE_SERVER_3",
	BUTTON_STATION_1: "BUTTON_STATION_1",
	BUTTON_STATION_2: "BUTTON_STATION_2",
	BUTTON_STATION_3: "BUTTON_STATION_3",
	BUTTON_VOLUME_DOWN: "BUTTON_VOLUME_DOWN",
	BUTTON_VOLUME_UP: "BUTTON_VOLUME_UP",
	SENSOR_THROTTLE: "SENSOR_THROTTLE",
	SENSOR_BRAKE: "SENSOR_BRAKE",
	ERROR_UNSPECIFIED: "ERROR_UNSPECIFIED",
	ERROR_NONE: "ERROR_NONE",
}

CanlibComponentIds = {
	"SCENARIO_BASELINE": SCENARIO_BASELINE,
	"SCENARIO_SECURE_INFOTAINMENT": SCENARIO_SECURE_INFOTAINMENT,
	"SCENARIO_SECURE_ECU": SCENARIO_SECURE_ECU,
	"FUNCTIONALITY_MINIMAL": FUNCTIONALITY_MINIMAL,
	"FUNCTIONALITY_MEDIUM": FUNCTIONALITY_MEDIUM,
	"FUNCTIONALITY_FULL": FUNCTIONALITY_FULL,
	"BESSPIN_TOOL_FREERTOS": BESSPIN_TOOL_FREERTOS,
	"FREERTOS_1": FREERTOS_1,
	"FREERTOS_2_CHERI": FREERTOS_2_CHERI,
	"FREERTOS_3": FREERTOS_3,
	"DEBIAN_1": DEBIAN_1,
	"DEBIAN_2_LMCO": DEBIAN_2_LMCO,
	"DEBIAN_3": DEBIAN_3,
	"TEENSY": TEENSY,
	"BESSPIN_TOOL_DEBIAN": BESSPIN_TOOL_DEBIAN,
	"IGNITION": IGNITION,
	"LED_COMPONENT": LED_COMPONENT,
	"CAN_DISPLAY": CAN_DISPLAY,
	"HACKER_KIOSK": HACKER_KIOSK,
	"HACK_NONE": HACK_NONE,
	"HACK_OTA": HACK_OTA,
	"HACK_BRAKE": HACK_BRAKE,
	"HACK_THROTTLE": HACK_THROTTLE,
	"HACK_TRANSMISSION": HACK_TRANSMISSION,
	"HACK_LKAS": HACK_LKAS,
	"HACK_INFOTAINMENT_VOLUME": HACK_INFOTAINMENT_VOLUME,
	"HACK_INFOTAINMENT_MUSIC": HACK_INFOTAINMENT_MUSIC,
	"INFOTAINMENT_THIN_CLIENT": INFOTAINMENT_THIN_CLIENT,
	"INFOTAINMENT_SERVER_1": INFOTAINMENT_SERVER_1,
	"INFOTAINMENT_SERVER_2": INFOTAINMENT_SERVER_2,
	"INFOTAINMENT_SERVER_3": INFOTAINMENT_SERVER_3,
	"OTA_UPDATE_SERVER_1": OTA_UPDATE_SERVER_1,
	"OTA_UPDATE_SERVER_2": OTA_UPDATE_SERVER_2,
	"OTA_UPDATE_SERVER_3": OTA_UPDATE_SERVER_3,
	"BUTTON_STATION_1": BUTTON_STATION_1,
	"BUTTON_STATION_2": BUTTON_STATION_2,
	"BUTTON_STATION_3": BUTTON_STATION_3,
	"BUTTON_VOLUME_DOWN": BUTTON_VOLUME_DOWN,
	"BUTTON_VOLUME_UP": BUTTON_VOLUME_UP,
	"SENSOR_THROTTLE": SENSOR_THROTTLE,
	"SENSOR_BRAKE": SENSOR_BRAKE,
	"ERROR_UNSPECIFIED": ERROR_UNSPECIFIED,
	"ERROR_NONE": ERROR_NONE,
}
