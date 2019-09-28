import unittest
import hashlib
from treehash import TreeHash

TEST_DATA = b"a"
TEST_CHUNK = 1
TEST_INDEX = 0


class TreeHashTestCase(unittest.TestCase):
    def test_constructor(self):
        self.assertEqual(
            TEST_CHUNK,
            len(TreeHash(TEST_CHUNK).hashes)
        )

    def test_update(self):
        tree_hash = TreeHash(TEST_CHUNK)
        tree_hash.update(TEST_DATA, TEST_INDEX)
        self.assertEqual(
            hashlib.sha256(TEST_DATA).hexdigest(),
            tree_hash.hexdigest()
        )

    def test_md5(self):
        tree_hash = TreeHash(TEST_CHUNK, algo=hashlib.md5)
        tree_hash.update(TEST_DATA, TEST_INDEX)
        self.assertEqual(
            hashlib.md5(TEST_DATA).hexdigest(),
            tree_hash.hexdigest()
        )

    def test_digest(self):
        tree_hash = TreeHash(TEST_CHUNK, algo=hashlib.md5)
        tree_hash.update(TEST_DATA, TEST_INDEX)
        self.assertEqual(
            hashlib.md5(TEST_DATA).digest(),
            tree_hash.digest()
        )

    def test_tree(self):
        hashlib_result = hashlib.sha256(
            hashlib.sha256(TEST_DATA).digest() +
            hashlib.sha256(TEST_DATA).digest()
        ).hexdigest()

        tree_hash = TreeHash(2, block_size=1)
        tree_hash.update(TEST_DATA, 0)
        tree_hash.update(TEST_DATA, 1)
        self.assertEqual(hashlib_result,
                         tree_hash.hexdigest())

    def test_empty(self):
        self.assertEqual(
            hashlib.sha256().hexdigest(),
            TreeHash(0).hexdigest()
        )
