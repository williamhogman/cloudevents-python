import json


def serialize(event):
    return json.dumps(event.to_dict())
