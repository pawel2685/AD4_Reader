from device_reader import PapouchReader
from routes import create_app
from waitress import serve
import argparse
import socket

def get_ip_address():
    """Get the primary IP address of the machine"""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Doesn't actually connect but gets the route
        s.connect(('8.8.8.8', 80))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Papouch AD4USB Reader Server')
    parser.add_argument('--port', type=str, default='COM3', help='Serial port for the device')
    parser.add_argument('--baudrate', type=int, default=115200, help='Baudrate for serial communication')
    parser.add_argument('--host', type=str, default='0.0.0.0', help='Host to bind the web server to')
    parser.add_argument('--web-port', type=int, default=8080, help='Port to run the web server on')
    args = parser.parse_args()
    
    # Initialize device reader
    reader = PapouchReader(port=args.port, baudrate=args.baudrate)
    
    # Start the reader in a background thread
    reader.start()
    
    # Create Flask app
    app = create_app(reader)
    
    # Get IP address information
    ip_address = get_ip_address()
    localhost_url = f"http://127.0.0.1:{args.web_port}"
    network_url = f"http://{ip_address}:{args.web_port}"
    
    # Start Waitress server
    print(f"\nPapouch AD4USB Reader Server")
    print(f"==============================")
    print(f"Device port: {args.port}")
    print(f"Baudrate: {args.baudrate}")
    print(f"\nServer is running at:")
    print(f"- Local URL: {localhost_url}")
    print(f"- Network URL: {network_url}")
    print(f"\nPress Ctrl+C to stop the server")
    print(f"==============================\n")
    
    try:
        serve(app, host=args.host, port=args.web_port)
    finally:
        # Make sure to stop the reader when the server is stopped
        reader.stop()
        print("\nServer stopped")

if __name__ == '__main__':
    main()