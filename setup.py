#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import setuptools
except ImportError:
    import distutils.core as setuptools

setuptools.setup(
    name='docker-registry-driver-glusterfs',
    version='0.0.1',
    author='Chen Chao',
    author_email='cc272309126@gmail.com',
    maintainer='Chen Chao',
    maintainer_email='cc272309126@gmail.com',
    url='https://github.com/cc272309126/docker-registry-driver-glusterfs',
    description='Docker registry glusterfs driver',
    long_description=open('./README.md').read(),
    download_url='https://github.com/cc272309126/docker-registry-driver-glusterfs/archive/master.zip',
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'Programming Language :: Python',
                 'Programming Language :: Python :: 2.6',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: Implementation :: CPython',
                 'Operating System :: OS Independent',
                 'Topic :: Utilities',
                 'License :: OSI Approved :: Apache Software License'],
    platforms=['Independent'],
    license=open('./LICENSE').read(),
    namespace_packages=['docker_registry', 'docker_registry.drivers'],
    packages=['docker_registry', 'docker_registry.drivers'],
    install_requires=open('./requirements.txt').read(),
    zip_safe=False,
)
