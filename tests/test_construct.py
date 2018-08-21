from cloudevents import create


class TestConstruct(object):
    def test_accepts_data(self):
        """Github issue #3"""
        evt = create("foo", "123", "bar", data="Hello", content_type="text/plain")
        assert evt.data == "Hello"
