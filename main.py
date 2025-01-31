import psutil
import serial
import serial.tools.list_ports
import time
import subprocess
import threading
import time

SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600
print('iniciando systemas chavales')

def run_c_restarter(device):
    # Assuming the compiled C program is 'program'
    print(f"restarting {device}")
    result = subprocess.run(["/usr/bin/usbreset", '2341:0043'], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("Output:\n", result.stdout)
    else:
        print("Error:\n", result.stderr)

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

# Try to open the serial connection
def connect_arduino_serial():
    try:
        port = detect_arduino() or SERIAL_PORT
    except Exception as e:
        print(f"Failed to detect port: {e}")
        return None  # Stop execution if port detection fails

    try:
        arduino = serial.Serial(port, BAUD_RATE)
        time.sleep(2)  # Allow Arduino time to reset
        print(f"Connected to {port}")
        return (arduino, port)
    except Exception as e:
        print(f"Failed to connect to {port}: {e}")

def get_fan_speed():
    try:
        fans = psutil.sensors_fans()
        if not fans:
            return None
        for fan_name, fan_data in fans.items():
            if fan_data and fan_data[0].current:
                return fan_data[0].current
    except Exception as e:
        print(f"Error reading fan speed: {e}")
    return None

def run_with_timeout(func, timeout):
    # Create a thread to run the function
    thread = threading.Thread(target=func)
    thread.start()

    # Wait for the thread to finish or timeout
    thread.join(timeout)

    if thread.is_alive():
        print("Timeout! The function took too long.")
        return False
        # The thread will continue running in the background if not handled properly
    return True

arduino, port = connect_arduino_serial()
print(f"arduino vale {arduino}, y port vale {port}")
while True:
    try:
        fan_speed = get_fan_speed()
        if fan_speed is not None:
            print(f"Fan speed: {fan_speed} RPM")

            write = lambda: arduino.write(f"{fan_speed}\n".encode())
            if not run_with_timeout(write, 30):
                run_c_restarter(port)
                arduino, port = connect_arduino_serial()
                print(f"reconneccion arduino vale {arduino}, y port vale {port}")
            arduino.flush()  # Ensure data is written out
            time.sleep(0.1)  # Give time to the serial buffer
        else:
            print("Fan speed not available.")
    except serial.SerialException as e:
        print(f"Serial error: {e}")
        break  # Exit loop if serial connection fails
    except Exception as e:
        print(f"Unexpected error: {e}")
        break

    time.sleep(2)

# Close the port properly when done
arduino.close()

