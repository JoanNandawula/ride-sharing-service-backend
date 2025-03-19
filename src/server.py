from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
from matching import find_nearest_driver
from api import update_driver_locations
import uuid
import threading
import time

# Load environment variables
load_dotenv()

app = Flask(__name__)

# In-memory database for simplicity
drivers = [
    {"id": "d1", "name": "John", "lat": 40.7128, "lon": -74.0060, "available": True},
    {"id": "d2", "name": "Sarah", "lat": 40.7300, "lon": -74.0100, "available": True},
    {"id": "d3", "name": "Mike", "lat": 40.7400, "lon": -73.9900, "available": True},
]

rides = {}

# Background task to update driver locations
def update_locations_task():
    while True:
        update_driver_locations(drivers)
        time.sleep(60)  # Update every minute

# Start the background task
location_updater = threading.Thread(target=update_locations_task, daemon=True)
location_updater.start()

# Root route to check API status
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Ride-Hailing API!"}), 200

@app.route('/request-ride', methods=['POST'])
def request_ride():
    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be application/json"}), 415

    data = request.get_json()
    if not data or 'lat' not in data or 'lon' not in data:
        return jsonify({"error": "Missing latitude or longitude"}), 400
    
    rider_lat = data['lat']
    rider_lon = data['lon']
    nearest_driver = find_nearest_driver(drivers, rider_lat, rider_lon)
    
    if not nearest_driver:
        return jsonify({"error": "No drivers available"}), 404
    
    ride_id = str(uuid.uuid4())
    rides[ride_id] = {
        "id": ride_id,
        "rider_lat": rider_lat,
        "rider_lon": rider_lon,
        "driver": nearest_driver,
        "status": "assigned"
    }
    
    for driver in drivers:
        if driver["id"] == nearest_driver["id"]:
            driver["available"] = False
            break
    
    return jsonify({"ride_id": ride_id, "driver": nearest_driver, "status": "assigned"}), 201

@app.route('/drivers', methods=['GET'])
def get_drivers():
    available_drivers = [driver for driver in drivers if driver["available"]]
    return jsonify(available_drivers), 200

@app.route('/ride-status/<ride_id>', methods=['GET'])
def get_ride_status(ride_id):
    ride = rides.get(ride_id)
    if not ride:
        return jsonify({"error": "Ride not found"}), 404
    return jsonify(ride), 200

@app.route('/complete-ride/<ride_id>', methods=['POST'])
def complete_ride(ride_id):
    ride = rides.get(ride_id)
    if not ride:
        return jsonify({"error": "Ride not found"}), 404
    
    ride["status"] = "completed"
    for driver in drivers:
        if driver["id"] == ride["driver"]["id"]:
            driver["available"] = True
            break
    
    return jsonify({"message": "Ride completed", "ride": ride}), 200

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=True)
