import json

def _check_not_null(d, name):
    if d.get(name) is None:
        raise RuntimeError("Missing required field {}".format(name))

def _check_non_empty_str(d, name):
    value = d.get(name)
    if value is None:
        return
    if not isinstance(value, str):
        raise RuntimeError("Field {} must be a string".format(name))
    if value == "":
        raise RuntimeError("Field {} must be a non-empty string".format(name))

FIELDS = [
    "eventType",
    "eventTypeVersion",
    "cloudEventsVersion",
    "source",
    "eventID",
    "eventTime",
    "schemaURL",
    "contentType",
    "extensions",
    "data"
]
FIELD_REMAPPING = {
    "event_type": "eventType",
    "event_type_version": "eventTypeVersion",
    "cloud_events_version": "cloudEventsVersion",
    "source": "source",
    "event_id": "eventID",
    "event_time": "eventTime",
    "schema_url": "schemaURL",
    "content_type": "contentType",
    "extensions": "extensions",
    "data": "data",
}
FIELD_REMAPPING_INV = {FIELD_REMAPPING[k]: k for k in FIELD_REMAPPING}

REQUIRED_FIELDS = ["eventType", "eventID", "source", "cloudEventsVersion"]
OPTIONAL_STRING_FIELDS = ["eventTypeVersion", "eventTime", "schemaURL", "contentType"]

def verify_cloudevent(d):
    for name in REQUIRED_FIELDS:
        _check_not_null(d, name)
        _check_non_empty_str(d, name)

    for name in OPTIONAL_STRING_FIELDS:
        _check_non_empty_str(d, name)

    ext = d.get("extensions")
    if ext and ext == {}:
        raise RuntimeError("Extensions must be non-empty or null")


class Event(object):
    def __init__(self, d):
        self.d = {k: d[k] for k in FIELDS if k in d}
        verify_cloudevent(self.d)

        if isinstance(self.d.get("data"), str):
            ct = self.content_type
            if (ct.startswith("application/json") or ct.endswith("+json")):
                self.d["data"] = json.loads(self.d["data"])

    def __getattribute__(self, name):
        if name in FIELD_REMAPPING:
            return self.d.get(FIELD_REMAPPING[name])
        else:
            return object.__getattribute__(self, name)

    def to_dict(self):
        return dict(self.d)

    @classmethod
    def create_from_dict(cls, d):
        return cls({FIELD_REMAPPING[k]: d[k] for k in d})
