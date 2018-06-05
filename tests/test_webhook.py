from nose.tools import eq_, raises
import requests_mock
from cloudevents import WebhookDestination, create

DEMO_EVENT = create("foo", "123", "hackerman")

DESTINATION = "https://destination"
class TestWebhook(object):
    def _wd(self):
        return WebhookDestination("origin", DESTINATION)
    def test_abuse_protection_allow(self):
        d = self._wd()
        with requests_mock.Mocker() as m:
            m.options(DESTINATION, status_code=200, headers={'WebHook-Allowed-Origin': '*'})
            assert d.may_send_webhook()

    def test_abuse_protection_deny(self):
        d = self._wd()
        with requests_mock.Mocker() as m:
            m.options(DESTINATION, status_code=500)
            assert not d.may_send_webhook()

    def test_abuse_protection_missing(self):
        d = self._wd()
        with requests_mock.Mocker() as m:
            m.options(DESTINATION, status_code=200)
            assert not d.may_send_webhook()


    @raises(RuntimeError)
    def test_abuse_protection_prevents_send(self):
        d = self._wd()
        with requests_mock.Mocker() as m:
            m.options(DESTINATION, status_code=200)
            assert not d.send(DEMO_EVENT)

    def test_sending_event_200(self):
        d = self._wd()
        code = 200
        with requests_mock.Mocker() as m:
            m.options(DESTINATION, status_code=200, headers={'WebHook-Allowed-Origin': '*'})
            m.post(DESTINATION, status_code=code)
            res = d.send(DEMO_EVENT)
            eq_(res, (code, ''))

    def test_sending_event_201(self):
        d = self._wd()
        code = 201
        with requests_mock.Mocker() as m:
            m.options(DESTINATION, status_code=200, headers={'WebHook-Allowed-Origin': '*'})
            m.post(DESTINATION, status_code=code)
            res = d.send(DEMO_EVENT)
            eq_(res, (code, ''))

    def test_sending_event_202(self):
        d = self._wd()
        code = 202
        with requests_mock.Mocker() as m:
            m.options(DESTINATION, status_code=200, headers={'WebHook-Allowed-Origin': '*'})
            m.post(DESTINATION, status_code=code)
            res = d.send(DEMO_EVENT)
            eq_(res, (code, ''))

    def test_sending_event_204(self):
        d = self._wd()
        code = 204
        with requests_mock.Mocker() as m:
            m.options(DESTINATION, status_code=200, headers={'WebHook-Allowed-Origin': '*'})
            m.post(DESTINATION, status_code=code)
            res = d.send(DEMO_EVENT)
            eq_(res, (code, ''))


    @raises(Exception)
    def test_sending_event_fail_500(self):
        d = self._wd()
        code = 500
        with requests_mock.Mocker() as m:
            m.options(DESTINATION, status_code=200, headers={'WebHook-Allowed-Origin': '*'})
            m.post(DESTINATION, status_code=code)
            d.send(DEMO_EVENT)

    @raises(Exception)
    def test_sending_event_fail_404(self):
        d = self._wd()
        code = 404
        with requests_mock.Mocker() as m:
            m.options(DESTINATION, status_code=200, headers={'WebHook-Allowed-Origin': '*'})
            m.post(DESTINATION, status_code=code)
            d.send(DEMO_EVENT)

    @raises(Exception)
    def test_sending_event_bad_2XX(self):
        d = self._wd()
        code = 250
        with requests_mock.Mocker() as m:
            m.options(DESTINATION, status_code=200, headers={'WebHook-Allowed-Origin': '*'})
            m.post(DESTINATION, status_code=code)
            d.send(DEMO_EVENT)
