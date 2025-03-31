import serial
import time

def read_ad4usb_channels_1_2(port='COM3', baudrate=115200):
    """
    Read data specifically from channels 1 and 2 of Papouch AD4USB device
    :param port: Serial port (COM port on Windows, /dev/ttyUSB* on Linux)
    :param baudrate: Baud rate (typically 115200 for AD4USB)
    :return: Dict with values from channels 1 and 2
    """
    # Open serial connection
    ser = serial.Serial(port, baudrate, timeout=1)
    
    try:
        # Clear any pending data
        ser.reset_input_buffer()
        
        # Command to read channels 1 and 2
        # In Spinel protocol, the command might differ slightly based on model
        # This example uses a general approach
        
        # For channel 1
        command_ch1 = bytes([0x2A, 0x61, 0x01, 0x01, 0x0D])  # Modify address as needed
        ser.write(command_ch1)
        time.sleep(0.1)
        response_ch1 = ser.read(100)
        
        # For channel 2
        command_ch2 = bytes([0x2A, 0x61, 0x02, 0x01, 0x0D])  # Modify address as needed
        ser.write(command_ch2)
        time.sleep(0.1)
        response_ch2 = ser.read(100)
        
        # Parse responses (adjust based on actual protocol)
        ch1_value = None
        ch2_value = None
        
        # Example parsing logic - adjust based on actual device response format
        if len(response_ch1) >= 6:
            ch1_value = (response_ch1[4] << 8) | response_ch1[5]
            
        if len(response_ch2) >= 6:
            ch2_value = (response_ch2[4] << 8) | response_ch2[5]
        
        return {
            "channel_1": ch1_value,
            "channel_2": ch2_value
        }
        
    finally:
        # Always close the serial connection
        ser.close()

# Example usage
if __name__ == "__main__":
    try:
        # Adjust the COM port based on your system
        readings = read_ad4usb_channels_1_2(port='COM3')
        
        print(f"Channel 1 reading: {readings['channel_1']}")
        print(f"Channel 2 reading: {readings['channel_2']}")
        
        # Convert to voltage if needed (assuming 10-bit ADC with 0-5V range)
        # Adjust the conversion formula based on your device specifications
        if readings['channel_1'] is not None:
            voltage_ch1 = readings['channel_1'] * (5.0/1023)
            print(f"Channel 1 voltage: {voltage_ch1:.3f}V")
            
        if readings['channel_2'] is not None:
            voltage_ch2 = readings['channel_2'] * (5.0/1023)
            print(f"Channel 2 voltage: {voltage_ch2:.3f}V")
        
    except Exception as e:
        print(f"Error: {e}")