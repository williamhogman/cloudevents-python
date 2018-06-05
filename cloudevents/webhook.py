"""Module for sending Cloud-Events Webhooks

This module implements sending of Events using the Cloud-Events
webhook format.
"""
def _requests_or_none():
    try:
        import requests
        return requests
    except ImportError:
        return None


def _requests_or_throw():
    r = _requests_or_none()
    if r is None:
        msg = "`requests` is not importable and no default implementation is provided"
        raise RuntimeError(msg)
    return r

def _default_post_fn():
    requests = _requests_or_throw()
    return requests.post


def _default_options_fn():
    requests = _requests_or_none()
    return requests.options


def origin_matches(our_origin, theirs):
    if theirs is None:
        return our_origin is None
    if theirs == "*":
        return True
    else:
        return our_origin.lower() == theirs.lower()


def _may_send_webhook_to(options_fn, origin, url):
    headers = {
        "WebHook-Request-Origin": origin,
    }
    res = options_fn(url, headers=headers)
    if not res.ok:
        return False
    else:
        theirs = res.headers.get("WebHook-Allowed-Origin")
        return origin_matches(origin, theirs)


def _send_cloud_event(post_fn, origin, url, json):
    headers = {
        'Origin': origin,
        'User-Agent': 'python-cloudevents'
    }
    return post_fn(url, headers=headers, json=json)


ALLOWED_STATUSES = set([200, 201, 202, 204])

class WebhookDestination(object):
    """Class representing a destination for webhooks

    `WebhookDestination` handles sending Cloud-Events using the
    webhook format to destinations. Unless disabled, the system checks
    for WebHook allowed origin before sending the first event.
    """
    def __init__(self, origin, consumer, enable_abuse_protection=True, post_fn=None, options_fn=None):
        """Constructs a new instance of WebhookDestination

        Accepts the current origin, the consumer URL to send to as
        well as an optional flag to disable abuse protection.
        """
        self.origin = origin
        self.consumer = consumer
        self.enable_abuse_protection = enable_abuse_protection
        self._options_fn = options_fn if options_fn else _default_options_fn()
        self._post_fn = post_fn if post_fn else _default_post_fn()
        self._may_send = not self.enable_abuse_protection

    def may_send_webhook(self):
        """Returns true if we may send webhooks to this destination.

        If abuse protection is disabled or the destination allows us
        to send requests this method will return true, otherwise false.
        """
        if self._may_send:
            return True

        return _may_send_webhook_to(
            self._options_fn,
            self.origin,
            self.consumer
        )

    def require_may_send(self):
        """Requires that we may send webhook to the destination

        Throws an exception if we're not allowed to send webhooks.
        """
        # Update _may_send state...
        self._may_send = self.may_send_webhook()
        # If still not true that means we may not send, throw an exception
        if not self._may_send:
            msg = "The origin {} is not allowed to send webhooks to {}".format(self.origin, self.consumer)
            raise RuntimeError(msg)

    def send(self, event):
        """Sends an event to the destination, checking abuse protection if required.

        If the response is a permissable CloudEvents webhook the
        status code and possible JSON body is returned. Otherwise, an
        exception is raised.
        """
        self.require_may_send()

        res = _send_cloud_event(
            self._post_fn,
            self.origin,
            self.consumer,
            event.to_dict()
        )
        res.raise_for_status()

        if res.status_code not in ALLOWED_STATUSES:
            msg = "Webhook destination returned status {}, which is not permissable according to spec".format(res.status)
            raise RuntimeError(msg)

        return (
            res.status_code,
            res.json()
            if res.headers.get('Content-Type') == "application/json"
            else res.content
            )
