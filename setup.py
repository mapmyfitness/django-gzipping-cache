from setuptools import setup, find_packages

setup(
    name='django-gzipping-cache',
    version='0.1.1',
    description='A wrapper for django caches that gzips cached values',
    long_description=open('README.rst').read(),
    author='MapMyFitness',
    author_email='coreteam@mapmyfitnessinc.com',
    url='https://github.com/mapmyfitness/django-gzipping-cache',
    download_url='https://pypi.python.org/pypi/django-gzipping-cache',
    license='BSD',
    packages=find_packages(exclude=('tests', 'example')),
    install_requires=[
        'Django>=1.3',
    ],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
