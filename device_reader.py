import serial

class AD4USBReader:
    def __init__(self, port="COM3", baudrate=9600, address="00"):
        self.port = port
        self.baudrate = baudrate
        self.address = address
        self.serial = serial.Serial(port, baudrate, timeout=1)

    def _build_command(self, channel):
        return f"@{self.address}RD{channel}#".encode()

    def _parse_response(self, response):
        try:
            response_str = response.decode().strip()
            if response_str.startswith(f"@{self.address}RD"):
                value = response_str.split("RD")[1].strip("#")
                return float(value)
        except Exception as e:
            print(f"Parse error: {e}")
        return None

    def read_input(self, channel):
        command = self._build_command(channel)
        self.serial.write(command)
        response = self.serial.readline()
        return self._parse_response(response)
