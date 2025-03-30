import serial
import time
import threading

class PapouchReader:
    def __init__(self, port='COM3', baudrate=115200):
        self.port = port
        self.baudrate = baudrate
        self.latest_readings = {
            "channel1": 0,
            "channel2": 0,
            "channel3": 0,
            "channel4": 0,
            "timestamp": 0
        }
        self.running = False
        self.thread = None
    
    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._read_loop, daemon=True)
            self.thread.start()
            return True
        return False
    
    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
        
    def get_readings(self):
        return self.latest_readings
    
    def _read_loop(self):
        ser = None
        try:
            ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                bytesize=8,
                parity='N',
                stopbits=1,
                timeout=1
            )
            
            while self.running:
                try:
                    # Command to get all channels using Spinel protocol
                    command = bytes([0x2A, 0x61, 0x00, 0x31, 0x0D])  # *a.1[CR]
                    ser.write(command)
                    
                    # Read response
                    response = ser.read(25)  # Adjust size as needed
                    
                    if len(response) >= 20:
                        # Parse the response
                        channel1 = int.from_bytes(response[4:6], byteorder='big', signed=True)
                        channel2 = int.from_bytes(response[8:10], byteorder='big', signed=True)
                        channel3 = int.from_bytes(response[12:14], byteorder='big', signed=True)
                        channel4 = int.from_bytes(response[16:18], byteorder='big', signed=True)
                        
                        # Update readings
                        self.latest_readings = {
                            "channel1": channel1,
                            "channel2": channel2,
                            "channel3": channel3,
                            "channel4": channel4,
                            "timestamp": time.time()
                        }
                    
                    time.sleep(1)  # Read every second
                except Exception as e:
                    print(f"Error reading from device: {e}")
                    time.sleep(5)  # Wait before trying again
        
        except Exception as e:
            print(f"Serial connection error: {e}")
        finally:
            if ser and ser.is_open:
                ser.close()