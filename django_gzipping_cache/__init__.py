from django.core.cache import get_cache
from cStringIO import StringIO
import gzip


# We don't inherit from BaseCache because we want __getattr__ to proxy everything
# to the real cache that we don't want to intercept
class GzippingCache(object):
    def __init__(self, params):
        super(GzippingCache, self).__init__(params)
        self._cache = get_cache(params.get('LOCATION'))
        self._compress_level = params.get('COMPRESS_LEVEL', 9)

    def gzip(self, value):
        buf = StringIO()
        gzip_file = gzip.GzipFile(mode='wb', compresslevel=self._compress_level, fileobj=buf)
        gzip_file.write(value)
        gzip_file.close()
        return buf.getvalue()

    def ungzip(self, value):
        buf = StringIO(value)
        gzip_file = gzip.GzipFile(mode='rb', fileobj=buf)
        result = gzip_file.read()
        gzip_file.close()
        return result

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
