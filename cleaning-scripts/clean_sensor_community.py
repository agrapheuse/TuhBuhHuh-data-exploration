from enum import Enum


class ValueTypes(str, Enum):
    P1 = "P1"
    P2 = "P2"
    HUMIDITY = "humidity"
    TEMPERATURE = "temperature"
    PRESSURE = "pressure"
    PRESSURE_AT_SEALEVEL = "pressure_at_sealevel"
    COUNTS = "counts"
    COUNTS_PER_MINUTE = "counts_per_minute"
    HV_PULSES = "hv_pulses"
    SAMPLE_TIME_MS = "sample_time_ms"
    NOISE_LAEQ = "noise_LAeq"
    NOISE_LA_MAX = "noise_LA_max"
    NOISE_LA_MIN = "noise_LA_min"
    CO2_PPM = "co2_ppm"

    def handle_value(value):
        match value["value_type"]:
            case ValueTypes.P1:
                return ValueTypes.handle_p1(value)
            case ValueTypes.P2:
                return ValueTypes.handle_p2(value)
            case ValueTypes.HUMIDITY:
                return ValueTypes.handle_humidity(value)
            case ValueTypes.TEMPERATURE:
                return ValueTypes.handle_temperature(value)
            case _:
                return None

    def handle_p1(p1):
        return p1

    def handle_p2(p2):
        return p2

    def handle_humidity(humidity):
        val = float(humidity["value"])
        if val < 0 or val > 100:
            return None
        return humidity

    def handle_temperature(temperature):
        val = float(temperature["value"])
        if val < -20:
            return None
        return temperature


def clean_record(record):
    new_values = []
    for value in record["sensordatavalues"]:
        new_values.append(ValueTypes.handle_value(value))

    if all(v is None for v in new_values):
        print("all of the vals were null so nothing returned")
        return None

    record["sensordatavalues"] = new_values

    return record


def clean_sensor_community_file(file):
    new_body = []
    for record in file["body"]:
        cleaned = clean_record(record)
        if cleaned is not None:
            new_body.append(cleaned)
    file["body"] = new_body
    return file
