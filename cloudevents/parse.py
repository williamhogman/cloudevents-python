import json
from cloudevents.model import Event


def parse(data):
    if isinstance(data, str):
        return Event(json.loads(data))
    else:
        return Event(data)
