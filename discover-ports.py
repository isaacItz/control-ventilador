import serial.tools.list_ports
import json
import pprint

# Lista todos los puertos disponibles
ports = serial.tools.list_ports.comports()

for port in ports:
    print(f"Puerto encontrado: {port.device} - {port.description} {port.hwid} ")
    print(vars(port))

def detect_arduino():
    ports = serial.tools.list_ports.comports()
    arduino_ports = [
        port.device
        for port in ports
        if 'Arduino' in port.description or 'ttyUSB' in port.device or 'ttyACM' in port.device
    ]

    if arduino_ports:
        print(f"Arduino detected on: {arduino_ports[0]}")
        return arduino_ports[0]
    else:
        print("No Arduino found")
        return None
