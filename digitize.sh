#! /usr/bin/env bash

set -euo pipefail

DEV=/dev/cu.usbserial-FTF06UDC

INIT="IN;SP4;"

SQUARE="IN;SP4;PA90,90;PD;PA90,900;PA900,900;PA900,90;PA90,90;PU;SP0;"

init_tty() {
    stty -f $DEV 9600 cs8 -cstopb -parenb
}

detect_status() {
    init_tty
    exec 3<>$DEV

    printf '\x1B.B' >&3
    IFS= read -t 0.1 -n6 bytes <&3
    if [[ $? -ne 0 ]]; then
        echo "Offline"
    else
        echo "Online"
    fi
    exec 3>&-
}

square() {
    echo "Prepare TTY"

    echo "Open FD"
    exec 3<>$DEV

    echo "Write"
    echo -n "$INIT" >&3

    echo "Close"
    exec 3>&-

    echo "Done"
}

detect_status
