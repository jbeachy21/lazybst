"""
CS3C, Assignment #4, lazy-delete binary tree tests
Jasper Beachy
"""

from assignment04 import *
from bst_test import *


# Inherit from the basic BST tests so all those should run.
class LazyBinarySearchTreeTestCase(BstTestCase):
    # Override class variable so all existing tests instantiate and test
    # LazyBinarySearchTree instead of BinarySearchTree
    TreeType = LazyBinarySearchTree

    # TODO add tests specifically for LazyBinarySearchTree
    def setUp(self):
        super().setUp()
        self.lazytree = self.TreeType([10, 5, 15])

    def test_remove_marks_node_as_deleted(self):
        self.lazytree.remove(5)
        self.assertFalse(5 in self.lazytree)
        self.assertEqual(self.lazytree._deleted_nodes, 1)
        self.assertEqual(self.lazytree._size, 2)

    def test_insert_reactivates_deleted_node(self):
        self.lazytree.remove(5)
        self.lazytree.insert(5)
        self.assertTrue(5 in self.lazytree)
        self.assertEqual(self.lazytree._deleted_nodes, 0)
        self.assertEqual(self.lazytree._size, 3)

    def test_collect_garbage_physically_removes_deleted_nodes(self):
        self.lazytree.remove(5)
        physical_before = self.lazytree.size_physical
        self.lazytree.collect_garbage()
        physical_after = self.lazytree.size_physical
        self.assertEqual(self.lazytree._deleted_nodes, 0)
        self.assertEqual(self.lazytree._size, 2)
        self.assertLess(physical_after, physical_before)
        self.assertFalse(5 in self.lazytree)

# Remove BstTestCase so it doesn't run against BinarySearchTree
del BstTestCase

if __name__ == '__main__':
    unittest.main()
