#!/usr/bin/env python3

import usb.core
import subprocess
import json
import time

VENDOR_ID = 0x5131
PRODUCT_ID = 0x2007
ENDPOINT_OUT = 0x01


def get_hardware_data():
    try:
        result = subprocess.run(
            ["sensors", "-j"],
            capture_output=True,
            text=True,
            check=True
        )

        data = json.loads(result.stdout)

        temp = data["k10temp-pci-00c3"]["Tctl"]["temp1_input"]
        rpm = data["it8628-isa-0a40"]["fan1"]["fan1_input"]

        return int(round(temp)), int(round(rpm))

    except Exception as e:
        print("Błąd sensors:", e)
        return 0, 0


def send_data(dev, temp, rpm):

    buffer = bytearray(64)

    # =========================
    # TEMPERATURA
    # =========================

    buffer[0] = 0x01
    buffer[1] = max(0, min(99, temp))

    # =========================
    # RPM - 16 bit
    # =========================

    rpm = max(0, min(65535, rpm))

    # BIG ENDIAN:
    # buffer[5] = starszy bajt
    # buffer[6] = młodszy bajt

    buffer[5] = (rpm >> 8) & 0xFF
    buffer[6] = rpm & 0xFF

    # =========================
    # USB
    # =========================

    dev.write(
        ENDPOINT_OUT,
        bytes(buffer),
        timeout=1000
    )

    print(
        f"TEMP: {temp} °C | "
        f"RPM: {rpm} | "
        f"buffer[5]: {buffer[5]} | "
        f"buffer[6]: {buffer[6]} | "
        f"HEX: {buffer[5]:02X} {buffer[6]:02X}"
    )


def main():

    print("Szukam MODECOM Volcano T102...")

    dev = usb.core.find(
        idVendor=VENDOR_ID,
        idProduct=PRODUCT_ID
    )

    if dev is None:
        print("Nie znaleziono urządzenia.")
        return

    print("Znaleziono MODECOM Volcano T102")

    try:
        if dev.is_kernel_driver_active(0):
            dev.detach_kernel_driver(0)
    except Exception:
        pass

    try:
        dev.set_configuration()
    except Exception:
        pass

    print("Uruchomiono.\n")

    while True:

        temp, rpm = get_hardware_data()

        send_data(dev, temp, rpm)

        time.sleep(2)


if __name__ == "__main__":
    main()
