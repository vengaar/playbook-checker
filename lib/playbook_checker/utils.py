
import yaml
import json

def to_json(data):
    return json.dumps(data, indent=2, sort_keys=True)

def read_config(path):
    with open(path) as fp:
        return yaml.safe_load(fp)
