from flask import Flask, jsonify, request
from flask_cors import CORS  # For handling CORS when your React app connects

def create_app(device_reader):
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    
    @app.route('/api/readings', methods=['GET'])
    def get_readings():
        return jsonify(device_reader.get_readings())
    
    # You might want to add other API endpoints as needed
    @app.route('/api/device-info', methods=['GET'])
    def get_device_info():
        # Example additional endpoint that provides device information
        return jsonify({
            "device": "Papouch AD4USB",
            "port": device_reader.port,
            "status": "connected" if device_reader.running else "disconnected"
        })
    
    return app