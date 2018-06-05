import requests_mock
from cloudevents import WebhookDestination

DESTINATION = "https://destination"
class TestWebhook(object):
    def test_abuse_protection_allow(self):
        d = WebhookDestination("origin", DESTINATION)
        with requests_mock.Mocker() as m:
            m.options(DESTINATION, status_code=200, headers={'WebHook-Allowed-Origin': '*'})
            assert d.may_send_webhook()

    def test_abuse_protection_deny(self):
        d = WebhookDestination("origin", "https://destination")
        with requests_mock.Mocker() as m:
            m.options(DESTINATION, status_code=500)
            assert not d.may_send_webhook()
