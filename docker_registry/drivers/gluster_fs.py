# -*- coding: utf-8 -*-
# Copyright (c) 2014 Docker.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
docker_registry.drivers.glusterfs
~~~~~~~~~~~~~~~~~~~~~~~~~~

This is a glusterfs filesystem based driver.

"""

import os
import shutil
import logging

from glusterfs import gfapi
from glusterfs import api

from ..core import driver
from ..core import exceptions
from ..core import lru

logger = logging.getLogger(__name__)

class GlusterFsCfg(object):
    def __init__(self):
        self.host = None
        self.volume = None

class Storage(driver.Base):

    supports_bytes_range = True

    def __init__(self, path=None, config=None):
        self._rootpath = path if path[0] == '/' else "/" + path 
        logger.info("the root path is %s" % self._rootpath)
        self.glusterfscfg = GlusterFsCfg()
        self.glusterfscfg.host = config.glusterfs_host
        self.glusterfscfg.volume = config.glusterfs_volume
        self._glustervol = gfapi.Volume(self.glusterfscfg.host, self.glusterfscfg.volume)
        mount_res = self._glustervol.mount()
        if mount_res != 0:
            logger.info("Mount the glusterfs %s:%s failed, it return %s" % (self.glusterfscfg.host, self.glusterfscfg.volume, mount_res))
        else:
            logger.info("Mount the glusterfs %s:%s success, it return %s" % (self.glusterfscfg.host, self.glusterfscfg.volume, mount_res))

    def _init_path(self, path=None, create=False):
        res = self._rootpath
        if not path:
            res = self._rootpath
        else:
            if path.startswith(self._rootpath):
                res = path
            else:
                res = os.path.join(self._rootpath, path)
        if create == True:
            dirname = os.path.dirname(res)
            if not self._glustervol.exists(dirname):
                self._glustervol.makedirs(dirname)
        return res
        
    @lru.get
    def get_content(self, path):
        path = self._init_path(path)
        is_exists = self._glustervol.exists(path)
        try:
            with self._glustervol.open(path, os.O_RDONLY) as f:
                data = f.read().raw
        except Exception:
            raise exceptions.FileNotFoundError('%s is not there' % path)

        return data

    @lru.set
    def put_content(self, path, content):
        path = self._init_path(path, create=True)
        with self._glustervol.open(path, os.O_WRONLY | os.O_CREAT ) as f:
            f.write(content)
        return path

    def stream_read(self, path, bytes_range=None):
        path = self._init_path(path)
        nb_bytes = 0
        total_size = 0
        try:
            with self._glustervol.open(path, os.O_RDWR) as f:
                if bytes_range:
                    f.lseek(bytes_range[0], os.SEEK_CUR)
                    total_size = bytes_range[1] - bytes_range[0] + 1
                logger.info("start to stream read %s" % path)
                while True:
                    buf = None
                    if bytes_range:
                        buf_size = self.buffer_size
                        if nb_bytes + buf_size > total_size:
                            buf_size = total_size - nb_bytes
                        if buf_size > 0:
                            buf = f.read(buf_size)
                            nb_bytes += len(buf)
                        else:
                            buf = ''
                    else:
                        buf = f.read(self.buffer_size)
                    if not buf:
                        break
                    yield buf.raw
        except IOError:
            raise exceptions.FileNotFoundError('%s is not there' % path)

    def stream_write(self, path, fp):
        path = self._init_path(path, create=True)
        with self._glustervol.open(path, os.O_RDWR | os.O_CREAT) as f:
            try:
                while True:
                    buf = fp.read(self.buffer_size)
                    logger.info("start to stream write %s" % path)
                    if not buf:
                        break
                    f.write(buf)
            except IOError:
                pass

    def list_directory(self, path=None):
        prefix = ''
        if path:
            prefix = '%s/' % path
        path = self._init_path(path)
        exists = False
        try:
            for d in self._glustervol.listdir(path):
                exists = True
                yield prefix + d
        except Exception:
            pass
        if not exists:
            raise exceptions.FileNotFoundError('%s is not there' % path)

    def exists(self, path):
        path = self._init_path(path)
        return self._glustervol.exists(path)

    @lru.remove
    def remove(self, path):
        path = self._init_path(path)
        if self._glustervol.isdir(path):
            self._glustervol.rmtree(path)
            return
        try:
            self._glustervol.unlink(path)
        except OSError:
            raise exceptions.FileNotFoundError('%s is not there' % path)

    def get_size(self, path):
        path = self._init_path(path)
        try:
            return self._glustervol.getsize(path)
        except OSError:
            raise exceptions.FileNotFoundError('%s is not there' % path)
