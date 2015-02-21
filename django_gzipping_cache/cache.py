from django.core.cache import get_cache
import pickle
import zlib


# We don't inherit from BaseCache because we want __getattr__
# to proxy everything to the real cache that we don't want to intercept
class GzippingCache(object):
    def __init__(self, location, params):
        super(GzippingCache, self).__init__()
        self._cache = get_cache(location)
        self._compress_level = params.get('COMPRESS_LEVEL', 6)
        self._pass_uncompressed = params.get('PASS_UNCOMPRESSED', False)

    def gzip(self, value):
        if not value:
            return None
        return zlib.compress(pickle.dumps(value), self._compress_level)

    def ungzip(self, value):
        if not value:
            return None
        try:
            return pickle.loads(zlib.decompress(value))
        except zlib.error:
            if self._pass_uncompressed:
                return value
            raise

    def __getattr__(self, name):
        return getattr(self._cache, name)

    def add(self, key, value, *args, **kwargs):
        value = self.gzip(value)
        return self._cache.add(key, value, *args, **kwargs)

    def get(self, *args, **kwargs):
        return self.ungzip(self._cache.get(*args, **kwargs))

    def set(self, key, value, *args, **kwargs):
        value = self.gzip(value)
        return self._cache.set(key, value, *args, **kwargs)

    def get_many(self, *args, **kwargs):
        value_dict = self._cache.get_many(*args, **kwargs)
        for k, v in value_dict.items():
            value_dict[k] = self.ungzip(v)

    def set_many(self, data, *args, **kwargs):
        for k, v in data.items():
            data[k] = self.gzip(v)
        self._cache.set_many(data, *args, **kwargs)
