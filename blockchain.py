''''Modul contains block chain implementation using linked list'''

from datetime import datetime
import hashlib

def calc_hash(string, **kws):
    '''Return hexadecimal digest of string using hash256'''
    return hashlib.sha256(string.encode(**kws)).hexdigest()


class Block:

    def __init__(self, data, timestamp=None, prev_hash=None):

        assert isinstance(timestamp, datetime), \
        'timestamp need to be datetime.datetime object'

        self.data = str(data)
        self.timestamp = timestamp if timestamp else datetime.now()
        self.prev_hash = hex(int(prev_hash, 16))[2:]
        self.hash = self._cacl_hash()
        self.prev_block = None

    def _cacl_hash(self, **kws):
        hash_string = self.data + str(self.timestamp) + self.prev_hash
        return calc_hash(hash_string, **kws)

class BlockChain:
    pass
