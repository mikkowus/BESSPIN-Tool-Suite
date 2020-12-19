#ifndef CANLIB_H
#define CANLIB_H

// rpmspin (float), maybe?
// J1939 compatible: NO
#define CAN_ID_RPMSPIN 0XAA0397AC
#define BYTE_LENGTH_RPMSPIN 4

// two_step (bool), maybe?
// Bounds/Range: 0/1
// J1939 compatible: NO
#define CAN_ID_TWO_STEP 0XAA2D94D7
#define BYTE_LENGTH_TWO_STEP 4

// Infotainment - Volume State (bool), required by Infotainment Server
// Bounds/Range: 0/1
// J1939 compatible: NO
// Description: 
//	0 = mute 
//	1 = volume
#define CAN_ID_INFOTAINMENT 0XAA2FEEF2
#define BYTE_LENGTH_INFOTAINMENT 1

// water_temperature (float), maybe?
// Units: C
// J1939 compatible: YES
// Description: 
//	Water temperature [C]
#define CAN_ID_WATER_TEMPERATURE 0XAA43A0C5
#define BYTE_LENGTH_WATER_TEMPERATURE 4

// tcs (int), maybe?
// J1939 compatible: NO
#define CAN_ID_TCS 0XAA5164AD
#define BYTE_LENGTH_TCS 4

// rpm_tacho (float), maybe?
// J1939 compatible: NO
#define CAN_ID_RPM_TACHO 0XAA7DD59E
#define BYTE_LENGTH_RPM_TACHO 4

// running (bool), maybe?
// Bounds/Range: 0/1
// J1939 compatible: NO
// Description: 
//	Engine running state
#define CAN_ID_RUNNING 0XAA7E1BAE
#define BYTE_LENGTH_RUNNING 4

// radiator_fan_spin (int), maybe?
// J1939 compatible: NO
#define CAN_ID_RADIATOR_FAN_SPIN 0XAA7FEC07
#define BYTE_LENGTH_RADIATOR_FAN_SPIN 4

// lightbar (int), maybe?
// J1939 compatible: NO
// Description: 
//	Lightbar state
#define CAN_ID_LIGHTBAR 0XAA86CF0A
#define BYTE_LENGTH_LIGHTBAR 4

// tcs_active (bool), maybe?
// Bounds/Range: 0/1
// J1939 compatible: NO
#define CAN_ID_TCS_ACTIVE 0XAAA17CD5
#define BYTE_LENGTH_TCS_ACTIVE 4

// lowpressure (int), maybe?
// J1939 compatible: NO
// Description: 
//	Low fuel pressure indicator
#define CAN_ID_LOWPRESSURE 0XAAA59DCF
#define BYTE_LENGTH_LOWPRESSURE 4

// Infotainment - Music State (bool), required by Infotainment Server
// Bounds/Range: 0/1
// J1939 compatible: NO
// Description: 
//	0 = pause 
//	1 = play
#define CAN_ID_INFOTAINMENT 0XAAAAB571
#define BYTE_LENGTH_INFOTAINMENT 1

// throttle_factor (int), maybe?
// J1939 compatible: NO
#define CAN_ID_THROTTLE_FACTOR 0XAABE5635
#define BYTE_LENGTH_THROTTLE_FACTOR 4

// car_y (float), required by Infotainment Server
// Units: m
// J1939 compatible: NO
// Description: 
//	infotainment position of car to display y coordinate
#define CAN_ID_CAR_Y 0XAABE5DF6
#define BYTE_LENGTH_CAR_Y 4

// parkingbrake (float), maybe?
// Bounds/Range: 0/1
// J1939 compatible: NO
// Description: 
//	Parking brake state. 0.5 = halfway on
#define CAN_ID_PARKINGBRAKE 0XAABFA005
#define BYTE_LENGTH_PARKINGBRAKE 4

// car_z (float), required by Infotainment Server
// Units: m
// J1939 compatible: NO
// Description: 
//	infotainment position of car to display z coordinate
#define CAN_ID_CAR_Z 0XAACC43BF
#define BYTE_LENGTH_CAR_Z 4

// rpm (float), maybe?
// Units: rpm
// J1939 compatible: YES
// Description: 
//	Engine RPM
#define CAN_ID_RPM 0XAAF00400
#define BYTE_LENGTH_RPM 4
#define PGN_RPM 61444
#define SPN_RPM 190

// gear (uint8_t), sent by ECU
// Bounds/Range: R, N, D, 1, 2, 3, 4, 5, 6
// J1939 compatible: YES
// Description: 
//	selected gear
#define CAN_ID_GEAR 0XAAF00500
#define BYTE_LENGTH_GEAR 1
#define PGN_GEAR 61445
#define SPN_GEAR 523

// steering (int), TODO
// J1939 compatible: YES
// Description: 
//	Steering state
#define CAN_ID_STEERING 0XAAF00900
#define BYTE_LENGTH_STEERING 4
#define PGN_STEERING 61449
#define SPN_STEERING 1807

// throttle_input (uint8_t), sent by ECU
// Bounds/Range: 0/255
// J1939 compatible: YES
// Description: 
//	Throttle input state
#define CAN_ID_THROTTLE_INPUT 0XAAF01A00
#define BYTE_LENGTH_THROTTLE_INPUT 1
#define PGN_THROTTLE_INPUT 61466
#define SPN_THROTTLE_INPUT 3464

// brake_intput (uint8_t), sent by ECU
// Bounds/Range: 0/255
// J1939 compatible: NO
// Description: 
//	Brake input state
#define CAN_ID_BRAKE_INTPUT 0XAAF01B00
#define BYTE_LENGTH_BRAKE_INTPUT 1
#define PGN_BRAKE_INTPUT 61467

// steering_input (int), TODO
// J1939 compatible: YES
// Description: 
//	Steering input state
#define CAN_ID_STEERING_INPUT 0XAAF01D00
#define BYTE_LENGTH_STEERING_INPUT 4
#define PGN_STEERING_INPUT 61469
#define SPN_STEERING_INPUT 3683

// reverse (int), maybe?
// J1939 compatible: NO
// Description: 
//	Reverse gear state
#define CAN_ID_REVERSE 0XAAF9AEF9
#define BYTE_LENGTH_REVERSE 4

// turnsignal (int), maybe?
// Bounds/Range: -1/1
// J1939 compatible: NO
// Description: 
//	Turn signal value. -1 = Left, 1 = Right,
//	gradually ‘fades’ between values. Use “signal_L” and “signal_R” for flashing indicators
#define CAN_ID_TURNSIGNAL 0XAAFAD8C4
#define BYTE_LENGTH_TURNSIGNAL 4

// oil (int), maybe?
// J1939 compatible: YES
#define CAN_ID_OIL 0XAAFC9F00
#define BYTE_LENGTH_OIL 4
#define PGN_OIL 64671
#define SPN_OIL 8856

// car_x (float), required by Infotainment Server
// Units: m
// J1939 compatible: NO
// Description: 
//	infotainment position of car to display x coordinate
#define CAN_ID_CAR_X 0XAAFCDACE
#define BYTE_LENGTH_CAR_X 4

// lowfuel (bool), maybe?
// Bounds/Range: 0/1
// J1939 compatible: YES
// Description: 
//	Low fuel indicator
#define CAN_ID_LOWFUEL 0XAAFD0400
#define BYTE_LENGTH_LOWFUEL 4
#define PGN_LOWFUEL 64772
#define SPN_LOWFUEL 5105

// lowhighbeam (int), maybe?
// J1939 compatible: NO
// Description: 
//	Low-high beam state
#define CAN_ID_LOWHIGHBEAM 0XAAFD6E6D
#define BYTE_LENGTH_LOWHIGHBEAM 4

// hazard (int), maybe?
// J1939 compatible: YES
#define CAN_ID_HAZARD 0XAAFDCC00
#define BYTE_LENGTH_HAZARD 4
#define PGN_HAZARD 64972
#define SPN_HAZARD 2875

// hazard_signal (bool), maybe?
// Bounds/Range: 0/1
// J1939 compatible: YES
#define CAN_ID_HAZARD_SIGNAL 0XAAFDCC00
#define BYTE_LENGTH_HAZARD_SIGNAL 4
#define PGN_HAZARD_SIGNAL 64972
#define SPN_HAZARD_SIGNAL 2875

// ignition (bool), maybe?
// Bounds/Range: 0/1
// J1939 compatible: YES
// Description: 
//	Engine state
#define CAN_ID_IGNITION 0XAAFDD400
#define BYTE_LENGTH_IGNITION 4
#define PGN_IGNITION 64980
#define SPN_IGNITION 10145

// headlights (int), maybe?
// J1939 compatible: YES
#define CAN_ID_HEADLIGHTS 0XAAFE4000
#define BYTE_LENGTH_HEADLIGHTS 4
#define PGN_HEADLIGHTS 65088
#define SPN_HEADLIGHTS 2350

// lights (int), maybe?
// Bounds/Range: 0/2
// J1939 compatible: YES
// Description: 
//	General light state. 1 = low, 2 = high
#define CAN_ID_LIGHTS 0XAAFE4000
#define BYTE_LENGTH_LIGHTS 4
#define PGN_LIGHTS 65088
#define SPN_LIGHTS 2404

// signal_l (int), maybe?
// Bounds/Range: 0/1
// J1939 compatible: YES
// Description: 
//	Left signal state. 0.5 = halfway to full blink
#define CAN_ID_SIGNAL_L 0XAAFE4000
#define BYTE_LENGTH_SIGNAL_L 4
#define PGN_SIGNAL_L 65088
#define SPN_SIGNAL_L 2368

// signal_r (int), duplicate ID!
// Bounds/Range: 0/1
// J1939 compatible: YES
// Description: 
//	Right signal state. 0.5 = halfway to full blink
#define CAN_ID_SIGNAL_R 0XAAFE4000
#define BYTE_LENGTH_SIGNAL_R 4
#define PGN_SIGNAL_R 65088
#define SPN_SIGNAL_R 2370

// left_signal (bool), maybe?
// Bounds/Range: 0/1
// J1939 compatible: YES
#define CAN_ID_LEFT_SIGNAL 0XAAFE4100
#define BYTE_LENGTH_LEFT_SIGNAL 4
#define PGN_LEFT_SIGNAL 65089
#define SPN_LEFT_SIGNAL 2367

// right_signal (bool), maybe?
// Bounds/Range: 0/1
// J1939 compatible: YES
#define CAN_ID_RIGHT_SIGNAL 0XAAFE4100
#define BYTE_LENGTH_RIGHT_SIGNAL 4
#define PGN_RIGHT_SIGNAL 65089
#define SPN_RIGHT_SIGNAL 2369

// wheelspeed (float), maybe?
// Units: m/s
// J1939 compatible: YES
// Description: 
//	Wheel speed [m/s]
#define CAN_ID_WHEELSPEED 0XAAFE6E00
#define BYTE_LENGTH_WHEELSPEED 4
#define PGN_WHEELSPEED 65134
#define SPN_WHEELSPEED 1592-1595

// oil_temperature (float), maybe?
// Units: C
// J1939 compatible: YES
// Description: 
//	Oil temperature [C]
#define CAN_ID_OIL_TEMPERATURE 0XAAFEEE00
#define BYTE_LENGTH_OIL_TEMPERATURE 4
#define PGN_OIL_TEMPERATURE 65262
#define SPN_OIL_TEMPERATURE 175

// throttle (int), maybe?
// J1939 compatible: YES
// Description: 
//	Throttle state
#define CAN_ID_THROTTLE 0XAAFEF200
#define BYTE_LENGTH_THROTTLE 4
#define PGN_THROTTLE 65266
#define SPN_THROTTLE 51

// parkingbrake_input (int), maybe?
// J1939 compatible: YES
// Description: 
//	Parking brake input state
#define CAN_ID_PARKINGBRAKE_INPUT 0XAAFEFA00
#define BYTE_LENGTH_PARKINGBRAKE_INPUT 4
#define PGN_PARKINGBRAKE_INPUT 65274
#define SPN_PARKINGBRAKE_INPUT 619

// fuel (uint8_t), required by Infotainment Server
// Bounds/Range: 0/100
// Units: %
// J1939 compatible: YES
// Description: 
//	Percentage of fuel remaining
#define CAN_ID_FUEL 0XAAFEFC00
#define BYTE_LENGTH_FUEL 1
#define PGN_FUEL 65276
#define SPN_FUEL 96

#endif