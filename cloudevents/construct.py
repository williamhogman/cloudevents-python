from cloudevents.model import Event
from cloudevents.constants import SPEC_VERSION


def create(
    event_type, event_id, source,
    cloud_events_version=SPEC_VERSION,
    event_type_version=None,
    event_time=None, schema_url=None, content_type=None
):
    return Event.create_from_dict(dict(
        event_type=event_type,
        event_id=event_id,
        source=source,
        cloud_events_version=cloud_events_version,
        event_type_version=event_type_version,
        event_time=event_time,
        schema_url=schema_url,
        content_type=content_type
    ))
