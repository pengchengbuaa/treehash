import sys
import hashlib
from io import BytesIO

MEGABYTE = 1024**2


class TreeHash(object):
    def __init__(self, chunck_n: int, algo=hashlib.sha256, block_size=MEGABYTE):
        self.algo = algo
        self.block_size = block_size
        self.hashes = [None] * chunck_n

    def _compute_hash(self):
        def recursive_hash(hashlist):
            output = [self.algo(h1.digest() + h2.digest())
                      for h1, h2 in zip(hashlist[::2], hashlist[1::2])]
            if len(hashlist) % 2:
                output.append(hashlist[-1])
            if len(output) > 1:
                return recursive_hash(output)
            return output[0]

        to_recurse = self.hashes[:]
        return recursive_hash(to_recurse or [self.algo(b"")])

    def update(self, data, index):
        self.hashes[index] = self.algo(data)

    def digest(self):
        return self._compute_hash().digest()

    def hexdigest(self):
        return self._compute_hash().hexdigest()
