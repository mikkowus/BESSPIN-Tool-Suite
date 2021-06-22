#!/bin/bash
PORT=5002
FOLDER=ecu_hacks/

mkdir -p ${FOLDER}

for TEST in --test ""
do
    for HACK_TYPE in throttle brake gear lkas
    do
        # Target1
        IP="10.88.88.12"
        SUFFIX="_baseline"
        # 1) ${HACK_TYPE}Nominal_baseline
        ./hack-ecu.py --port $PORT --type $HACK_TYPE --ip $IP --nominal ${TEST}
        mv j1939hack/hack.elf ${FOLDER}${HACK_TYPE}Nominal${SUFFIX}${TEST}.elf
        # 2) ${HACK_TYPE}Hacked_baseline
        ./hack-ecu.py --port $PORT --type $HACK_TYPE --ip $IP ${TEST}
        mv j1939hack/hack.elf ${FOLDER}${HACK_TYPE}Hacked${SUFFIX}${TEST}.elf

        # Target2
        IP="10.88.88.22"
        SUFFIX="_ssithInfo"
        # 1) ${HACK_TYPE}Nominal_baseline
        ./hack-ecu.py --port $PORT --type $HACK_TYPE --ip $IP --nominal ${TEST}
        mv j1939hack/hack.elf ${FOLDER}${HACK_TYPE}Nominal${SUFFIX}${TEST}.elf
        # 2) ${HACK_TYPE}Hacked_baseline
        ./hack-ecu.py --port $PORT --type $HACK_TYPE --ip $IP ${TEST}
        mv j1939hack/hack.elf ${FOLDER}${HACK_TYPE}Hacked${SUFFIX}${TEST}.elf

        # Target3
        IP="10.88.88.32"
        SUFFIX="_ssithEcu"
        # 1) ${HACK_TYPE}Nominal_baseline
        ./hack-ecu.py --port $PORT --type $HACK_TYPE --ip $IP --nominal ${TEST}
        mv j1939hack/hack.elf ${FOLDER}${HACK_TYPE}Nominal${SUFFIX}${TEST}.elf
        # 2) ${HACK_TYPE}Hacked_baseline
        ./hack-ecu.py --port $PORT --type $HACK_TYPE --ip $IP ${TEST}
        mv j1939hack/hack.elf ${FOLDER}${HACK_TYPE}Hacked${SUFFIX}${TEST}.elf
    done
done