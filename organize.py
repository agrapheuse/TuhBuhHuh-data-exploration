#!/Users/tomellm/.pyenv/shims/python
import json
import os
from enum import Enum
from api_functions import parse_open_sense_map, parse_sensor_community, parse_telraam


class Apis(str, Enum):

    OPEN_SENSE_MAP = "2889936e-8e2d-11ee-b9d1-0242ac120002"
    SENSOR_COMMUNITY = "017f12f5-8acb-4531-ab77-0e5208a31bca"
    TELRAAM = "8c9a8f25-e54e-4884-aee6-a4529c5424ba"


data_dir = "./all_data"
out_dir = "./all_out"


def filter_body(endpoint, body):
    match endpoint:
        case Apis.OPEN_SENSE_MAP:
            return None # parse_open_sense_map(body)
        case Apis.SENSOR_COMMUNITY:
            return parse_sensor_community(body)
        case Apis.TELRAAM:
            return parse_telraam(body)
        case _:
            print(f"ERROR: missing parsing implementation for endpoint {endpoint}")
            return None


dirs = os.listdir(data_dir)
for dir in dirs:
    for file in os.listdir(f"{data_dir}/{dir}"):
        with open(f"{data_dir}/{dir}/{file}") as f:
            str_file = f.read()
            response = json.loads(str_file)
            new_body = filter_body(dir, response["body"])
            if new_body != None: 
                response["body"] = new_body
                if not os.path.exists(f"{out_dir}/{dir}/"):
                    os.makedirs(f"{out_dir}/{dir}/")
                with open(f"{out_dir}/{dir}/{file}", "w") as o:
                    o.write(json.dumps(response))

