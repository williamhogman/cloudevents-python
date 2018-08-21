from cloudevents import create


class TestConstruct(object):
    def test_accepts_data(self):
        """Github issue #3"""
        evt = create("foo", "123", "bar", data="Hello", content_type="text/plain")
        assert evt.data == "Hello"

    def test_json_decoding_not_attempted_when_content_type_is_none(self):
        # Regression for bug caused when content_type is None
        evt = create("foo", "123", "bar", data="Hello")
        assert evt.data == "Hello"
