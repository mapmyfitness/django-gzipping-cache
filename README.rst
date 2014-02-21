=====================
Django Gzipping Cache
=====================

The Django Gzipping Cache is a transparent wrapper of django caches that
gzips values before they are sent to the underlying cache.

Django Gzipping Cache is released under the BSD license, like Django.
If you like it, please consider contributing!

===
Use
===

The gzipping cache is declared like so::

    CACHES = {
        ...
        'my_cache': {
            'BACKEND': 'django_gzipping_cache.cache.GzippingCache',
            'LOCATION': '_my_cache'
        },
        '_my_cache': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'snowflake'
        },
        ...
    })

This will create 2 caches, one is a standard LocMemCache (though GzippingCache
will wrap any django cache) and the other is a gzip cache. Here's a sample
iPython run with the above::

    In [1]: from django.core.cache import get_cache

    In [2]: my_cache = get_cache('my_cache')

    In [3]: _my_cache = get_cache('_my_cache')

    In [4]: my_cache.set('foo', 'bar')

    In [5]: my_cache.get('foo')
    Out[5]: 'bar'

    In [6]: _my_cache.get('foo')
    Out[6]: 'x\x9cKJ,\x02\x00\x02]\x016'

Obviously, you should not use the GzippingCache for small strings as gzip output
can be longer.

=============
Configuration
=============

GzippingCache takes 2 additional parameters, the default configuration is::

    CACHES = {
        ...
        'my_cache': {
            'BACKEND': 'django_gzipping_cache.cache.GzippingCache',
            'LOCATION': '_my_cache'
            'COMPRESS_LEVEL': 6,
            'PASS_UNCOMPRESSED': False,
        },
        ...
    })

COMPRESS_LEVEL is the number from 1-9 that tells zlib how aggressively to compress,
higher numbers take more CPU in order to achieve smaller output.

PASS_UNCOMPRESSED is for storing compressed and uncompressed data in the same
underlying cache. This is not recommended. If PASS_UNCOMPRESSED is set to True and
a piece of data fails a CRC check, the data will be returned. If the data was corrupted
this will most likely result in your application misbehaving.
