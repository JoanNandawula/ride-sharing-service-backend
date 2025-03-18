# src/matching.py
import math

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

def find_nearest_driver(drivers, rider_lat, rider_lon):
    """
    Find the nearest available driver to the rider using the Haversine formula
    """
    nearest_driver = None
    min_distance = float('inf')
    
    for driver in drivers:
        if driver["available"]:
            distance = haversine_distance(
                rider_lat, rider_lon,
                driver["lat"], driver["lon"]
            )
            
            if distance < min_distance:
                min_distance = distance
                nearest_driver = driver.copy()  # Create a copy to avoid modifying the original
                nearest_driver["distance"] = round(distance, 2)
    
    return nearest_driver