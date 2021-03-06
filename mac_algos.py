# Copyright 2018 Henry-Joseph Audéoud & Timothy Claeys
#
# This file is part of mini-ssh.
#
# mini-ssh is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# mini-ssh is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with mini-ssh.  If not, see
# <https://www.gnu.org/licenses/>.

import abc
import hashlib
import hmac


class MacAlgo(metaclass=abc.ABCMeta):
    supported = {}  # All supported algo names

    @property
    @abc.abstractmethod
    def name(self):
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def mac_length(self):
        raise NotImplementedError()

    def __init_subclass__(cls):
        super().__init_subclass__()
        MacAlgo.supported[cls.name] = cls

    @abc.abstractmethod
    def compute_mac(self, payload) -> bytes:
        """Compute the MAC of this payload"""
        raise NotImplementedError()

    def check_mac(self, payload, mac):
        """Raise Exception if given MAC is invalid for this payload."""
        if self.compute_mac(payload) != mac:
            raise Exception("Incorrect MAC detected")


class NoneMAC(MacAlgo):
    """MAC of any message is empty.

    This is the default algorithm, when a connection is started."""
    _name = "none"
    _mac_length = 0

    @property
    def name(self):
        return self._name

    @property
    def mac_length(self):
        return self._mac_length

    def compute_mac(self, payload):
        return b""

    def check_mac(self, payload, mac):
        return mac == b""


class HmacSha2_256(MacAlgo):
    _name = "hmac-sha2-256"
    _mac_length = 32

    def __init__(self, key):
        self.key = key

    @property
    def name(self):
        return self._name

    @property
    def mac_length(self):
        return self._mac_length

    def compute_mac(self, payload):
        return hmac.HMAC(self.key, payload, hashlib.sha256).digest()[:32]
