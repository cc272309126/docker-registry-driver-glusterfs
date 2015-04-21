# Docker registry GlusterFs driver
==================================

This is a
[docker-registry backend driver](https://github.com/dotcloud/docker-registry/tree/master/depends/docker-registry-core)
for GlusterFS.

## Usage
========
Assuming you have a working docker-registry and libgfapi setup(you can get it here： https://codeload.github.com/gluster/libgfapi-python/zip/master).

    get source code and run:
    python setup.py install

Edit your configuration so that storage reads glusterfs options.

## Config
=========
You should add all the following configurations to your main docker-registry configuration to further configure it, which by default is  config/config.yml.

    glusterfs configrations:
        * storage: specify the storage to use
        * storage_path: specify the path prefix of the glusterfs you select
        * glusterfs_host: specify the host of gluterfs you select
        * glusterfs_volume: specify the vloume of glusterfs you select

    example <you can copy this example into your config.yml, and modify it accordingly>:

    glusterfs: &glusterfs
        <<: *common
        storage: gluster_fs
        storage_path: _env:STORAGE_PATH
        glusterfs_host: _env:GLUSTERFS_HOST
        glusterfs_volume: _env:GLUSTERFS_VOLUME

