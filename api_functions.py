#!/Users/tomellm/.pyenv/shims/python
import json
from enum import Enum

class Bounds(float, Enum):
    MIN_LAT = 52.39290011580509
    MAX_LAT = 52.5730
    MIN_LNG = 13.2770
    MAX_LNG = 13.571993619688197

    def in_bounds(lat: float, lng: float) -> bool:
        lat = float(lat)
        lng = float(lng)
        return (lat != None and lng != None
            and Bounds.MIN_LAT <= lat and lat <= Bounds.MAX_LAT
            and Bounds.MIN_LNG <= lng and lng <= Bounds.MAX_LNG)


def parse_open_sense_map(body):
    body = json.loads(body)
    # print(f"The original length is {len(body)}")
    sensors = []
    for sensor in body:
        coordinates = sensor["currentLocation"]["coordinates"]
        if Bounds.in_bounds(coordinates[0],coordinates[1]):
            sensors.append(sensor)
    # print(f"The final length is {len(sensors)}")
    return sensors


def parse_sensor_community(body):
    body = json.loads(body)
    # print(f"The original length is {len(body)}")
    sensors = []
    for sensor in body:
        location = sensor["location"]
        if Bounds.in_bounds(location["latitude"],location["longitude"]):
            sensors.append(sensor)
    # print(f"The final length is {len(sensors)}")
    return sensors


def check_gtelraam_geometry(geometry) -> bool:

    def actual_bounds_check(point) -> bool:
        return Bounds.in_bounds(point[1], point[0])

    for inner_geometry in geometry:
        for point in inner_geometry:
            if actual_bounds_check(point):
                return True
    return False


def parse_telraam(body):
    body = json.loads(body)
    items = len(body["features"])
    print(f"The original length is {items}")
    sensors = []
    for sensor in body["features"]:
        if check_gtelraam_geometry(sensor["geometry"]["coordinates"]):
            sensors.append(sensor)
    # print(f"The final length is {len(sensors)}")
    body["features"] = sensors
    return body
