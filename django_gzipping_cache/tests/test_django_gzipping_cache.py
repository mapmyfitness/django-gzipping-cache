import unittest
from mock import MagicMock, patch

with patch('django.conf.settings') as settings:
    settings.CACHES = {
        'default': {'BACKEND': 'django.core.cache.backends.dummy.DummyCache'}
    }
    from ..cache import GzippingCache


class TestCacheFunctions(unittest.TestCase):

    @patch('django_gzipping_cache.cache.get_cache')
    def setUp(self, get_cache):
        self.underlying = MagicMock()
        get_cache.return_value = self.underlying
        params = {'LOCATION': 'foo', 'PASS_UNCOMPRESSED': True}
        self.cache = GzippingCache(params)

    def test_add_passes_through(self):
        self.cache.add('foo', 'bar')
        self.assertTrue(self.underlying.add.called)

    def test_get_passes_through_uncompressed_data(self):
        self.underlying.get.return_value = 'bar'
        value = self.cache.get('foo')
        self.assertTrue(self.underlying.get.called)
        self.assertEqual('bar', value)

    def test_get_passes_none_through(self):
        self.underlying.get.return_value = None
        val = self.cache.get('foo')
        self.assertIsNone(val)
        self.assertTrue(self.underlying.get.called)

    def test_get_many_passes_through(self):
        self.cache.get_many('foo', 'bar')
        self.underlying.get_many.assert_called_once_with('foo', 'bar')

    def test_make_key_passes_through(self):
        self.cache.make_key('foo')
        self.underlying.make_key.assert_called_once_with('foo')

    def test_arbitrary(self):
        self.cache.nonesuch_method('foo', 'bar')
        self.assertTrue(self.underlying.nonesuch_method.called)

    def test_round_trip_simple(self):
        start_value = 'test_string'
        self.cache.set('meta', start_value)
        stored_value = self.underlying.set.call_args[0][1]
        self.underlying.get.return_value = stored_value
        end_value = self.cache.get('meta')
        self.assertEqual(start_value, end_value)

    def test_round_trip_complex(self):
        with open(__file__, 'r') as f:
            start_value = f.read()
            self.cache.set('meta', start_value)
            stored_value = self.underlying.set.call_args[0][1]
            self.underlying.get.return_value = stored_value
            end_value = self.cache.get('meta')
            self.assertEqual(start_value, end_value)
