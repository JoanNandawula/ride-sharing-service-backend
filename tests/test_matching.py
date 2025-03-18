# tests/test_matching.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.matching import haversine_distance, find_nearest_driver

def test_haversine_distance():
    # Test with known distances
    # New York to Los Angeles ~3,944 km
    distance = haversine_distance(40.7128, -74.0060, 34.0522, -118.2437)
    assert 3900 < distance < 4000
    
    # Same location should be 0
    distance = haversine_distance(40.7128, -74.0060, 40.7128, -74.0060)
    assert distance == 0

def test_find_nearest_driver():
    # Test data
    drivers = [
        {"id": "d1", "name": "Driver1", "lat": 40.7128, "lon": -74.0060, "available": True},
        {"id": "d2", "name": "Driver2", "lat": 40.7300, "lon": -74.0100, "available": True},
        {"id": "d3", "name": "Driver3", "lat": 40.7400, "lon": -73.9900, "available": False},  # Not available
    ]
    
    # Test finding nearest available driver
    rider_lat, rider_lon = 40.7200, -74.0050
    nearest = find_nearest_driver(drivers, rider_lat, rider_lon)
    
    assert nearest is not None
    assert nearest["id"] == "d1"  # Driver1 should be closest
    assert "distance" in nearest
    
    # Test with no available drivers
    for driver in drivers:
        driver["available"] = False
    
    nearest = find_nearest_driver(drivers, rider_lat, rider_lon)
    assert nearest is None

# tests/test_api.py
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.api import update_driver_locations, geocode_address
from unittest.mock import patch, MagicMock

def test_update_driver_locations():
    # Test data
    drivers = [
        {"id": "d1", "name": "Driver1", "lat": 40.7128, "lon": -74.0060, "available": True},
        {"id": "d2", "name": "Driver2", "lat": 40.7300, "lon": -74.0100, "available": True},
    ]
    
    # Store original locations
    original_locations = [(d["lat"], d["lon"]) for d in drivers]
    
    # Update locations
    update_driver_locations(drivers)
    
    # Check that locations have changed
    new_locations = [(d["lat"], d["lon"]) for d in drivers]
    assert new_locations != original_locations

@patch('requests.get')
def test_geocode_address(mock_get):
    # Mock the API response
    mock_response = MagicMock()
    mock_response.json.return_value = [{"lat": "40.7128", "lon": "-74.0060"}]
    mock_get.return_value = mock_response
    
    # Test geocoding
    lat, lon = geocode_address("New York")
    assert lat == 40.7128
    assert lon == -74.0060
    
    # Test with no results
    mock_response.json.return_value = []
    result = geocode_address("NonexistentLocation")
    assert result is None