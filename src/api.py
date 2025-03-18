# src/api.py
import requests
import os
import random
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def update_driver_locations(drivers):
    """
    Update driver locations using the OpenStreetMap Nominatim API
    In a real application, this would connect to a real-time service
    For demo purposes, we'll:
    1. Use OpenStreetMap API to get coordinates of locations
    2. Simulate drivers moving by slightly modifying their coordinates
    """
    # For demonstration, we'll slightly modify the coordinates
    # In a real application, this would fetch real-time data
    for driver in drivers:
        # Simulate movement by adding a small random offset
        # In a real app, this would come from a real-time tracking system
        lat_offset = random.uniform(-0.002, 0.002)
        lon_offset = random.uniform(-0.002, 0.002)
        
        driver["lat"] += lat_offset
        driver["lon"] += lon_offset

def geocode_address(address):
    """
    Convert an address to latitude and longitude using OpenStreetMap Nominatim API
    """
    try:
        # Nominatim API endpoint
        url = f"https://nominatim.openstreetmap.org/search?q={address}&format=json&limit=1"
        
        # Add user agent to comply with OSM usage policy
        headers = {
            "User-Agent": "RideSharingApp/1.0"
        }
        
        response = requests.get(url, headers=headers)
        data = response.json()
        
        if data:
            lat = float(data[0]["lat"])
            lon = float(data[0]["lon"])
            return lat, lon
        else:
            return None
    except Exception as e:
        print(f"Error geocoding address: {e}")
        return None

def get_route(start_lat, start_lon, end_lat, end_lon):
    """
    Get a route between two points using OpenStreetMap Routing API (OSRM)
    """
    try:
        # OSRM API endpoint
        url = f"http://router.project-osrm.org/route/v1/driving/{start_lon},{start_lat};{end_lon},{end_lat}?overview=full&geometries=geojson"
        
        response = requests.get(url)
        data = response.json()
        
        if data["code"] == "Ok":
            # Extract route information
            route = data["routes"][0]
            distance = route["distance"]  # in meters
            duration = route["duration"]  # in seconds
            geometry = route["geometry"]  # GeoJSON geometry
            
            return {
                "distance": distance,
                "duration": duration,
                "geometry": geometry
            }
        else:
            return None
    except Exception as e:
        print(f"Error getting route: {e}")
        return None