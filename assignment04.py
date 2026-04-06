"""
CS3C, Assignment #4, lazy-delete binary tree
Jasper Beachy
"""

from bst import *


class LazyBinaryTreeNode(BinaryTreeNode):
    def __init__(self, data, deleted=False, left_child=None, right_child=None):
        self._deleted = deleted
        super().__init__(data, left_child, right_child)

    @property
    def deleted(self):
        return self._deleted

    @deleted.setter
    def deleted(self, deleted):
        self._deleted = deleted

    def __str__(self):
        return f"{self.data} (D)" if self.deleted else str(self.data)

    def __repr__(self):
        return f"LazyBinaryTreeNode(data={self.data}, deleted={self._deleted})"

class LazyBinarySearchTree(BinarySearchTree):
    TreeNode = LazyBinaryTreeNode
    def __init__(self, iterable=None):
        super().__init__()
        self._deleted_nodes = 0

        if iterable:
            for item in iterable:
                self.insert(item)

    @property
    def size_logical(self):
        return self._size

    @property
    def size_physical(self):
        return self._count_physical(self._root)

    def _count_physical(self, node):
        if node is None:
            return 0
        return 1 + self._count_physical(node.left_child) + self._count_physical(node.right_child)

    def find(self, data):
        node = self._find_node(data)
        if node.deleted or node is None:
            raise BinarySearchTree.NotFoundError
        return node.data

    def _find_max_valid(self, node):
        if node is None:
            return None
        right = self._find_max_valid(node.right_child)
        if right is not None:
            return right
        if not node.deleted:
            return node.data
        return self._find_max_valid(node.left_child)

    def find_max(self):
        node = self._root
        result = self._find_max_valid(node)
        if result is None:
            raise BinarySearchTree.EmptyTreeError
        return result

    def _find_min_valid(self, node):
        if node is None:
            return None
        left = self._find_min_valid(node.left_child)
        if left is not None:
            return left
        if not node.deleted:
            return node.data
        return self._find_min_valid(node.right_child)

    def find_min(self):
        node = self._root
        result = self._find_min_valid(node)
        if result is None:
            raise BinarySearchTree.EmptyTreeError
        return result

    def insert(self, data):
        try:
            node = self._find_node(data)
            # if the node is "deleted" then we turn it back on like a light switch
            if node.deleted:
                node.deleted = False
                self._deleted_nodes -= 1
                self._size += 1
            # If not deleted, it's a duplicate, so raise error
            else:
                raise BinarySearchTree.DuplicateDataError(f"{data} already exists.")
            # we use an exception for not found error to clearly signal a value is
            # not in the tree.  this helps to distinguish between:
            # a node that exists
            # and a node that does not exist
            # returning none in a tree alternatively could mean many different things
            # this makes it unambiguous albeit confusing at first glance
        except BinarySearchTree.NotFoundError:
            super().insert(data)


    def collect_garbage(self):

        if self._deleted_nodes == 0:
            print("No garbage collected")
            return
        self._root = self._collect(self._root)
        # After physically removing deleted nodes, recalc sizes
        self._deleted_nodes = 0
        self._recalculate_logical_size()


    def _collect(self, node):
        # Base case: reached a leaf node
        if node is None:
            return None
        # Recursively clean up left and right subtrees
        node.left_child = self._collect(node.left_child)
        node.right_child = self._collect(node.right_child)
        # If current node is marked as deleted, remove it physically
        if node.deleted:
            self._size -= 1
            self._deleted_nodes -= 1
            # Replace the deleted node with the correct child or restructure subtree
            return self._physically_remove_node(node)
        # Return the current node unchanged
        return node

    def _physically_remove_node(self, node):
        # Case 1: no left child - just return the right child
        if node.left_child is None:
            return node.right_child
        # Case 2: no right child just return the left child
        if node.right_child is None:
            return node.left_child

        # Case 3: two children - replace node's data with the largest value
        # from the left subtree (in-order) then delete that node
        max_node_parent = node
        max_node = node.left_child
        # find the rightmost node in the left subtree
        while max_node.right_child:
            max_node_parent = max_node
            max_node = max_node.right_child
        # Copy max value into the current node
        node.data = max_node.data
        node.deleted = False
        # Recursively remove the node just copied
        if max_node_parent == node:
            # If max node was directly the left child
            node.left_child = self._collect(max_node.left_child)
        else:
            # Otherwise adjust parent's right child
            max_node_parent.right_child = self._collect(max_node.left_child)

        return node

    def _recalculate_logical_size(self):
        def count_logical(node):
            if node is None:
                return 0
            left_count = count_logical(node.left_child)
            right_count = count_logical(node.right_child)
            return (0 if node.deleted else 1) + left_count + right_count

        self._size = count_logical(self._root)

    def remove(self, data):
        node = self._find_node(data)
        if node is None or node.deleted:
            raise LazyBinarySearchTree.NotFoundError(f"Value {data} not found or already deleted")

        node.deleted = True
        self._deleted_nodes += 1
        self._size -= 1

    def __contains__(self, item):
        try:
            node = self._find_node(item)
            return node is not None and not node.deleted
        except BinarySearchTree.NotFoundError:
            return False

    def _str(self, subtree_root, depth, _repr=False):
        if subtree_root is None:
            return ""
        s = ""
        s += self._str(subtree_root.right_child, depth + 1, _repr)
        display = repr(subtree_root) if _repr else str(subtree_root)
        s += " " * 4 * depth + display + "\n"
        s += self._str(subtree_root.left_child, depth + 1, _repr)
        return s


    def __str__(self):
        return f"{self.__class__.__name__} size={self._size}\n" + self._str(self._root, 0)

    def _iter(self, node):
        if node is None:
            return
        yield from self._iter(node.left_child)
        if not node.deleted:
            yield node.data
        yield from self._iter(node.right_child)

    def __iter__(self):
        return self._iter(self._root)

    def __len__(self):
        return self._size

    def __repr__(self):
        return (f"{self.__class__.__name__}(size={self._size}, "
                f"size_physical={self.size_physical})\n" +
                self._str(self._root, 0, _repr=True))


def show_test(title, expected, actual, original=None):
    print("=" * 40)
    print(f"{title}")
    if original is not None:
        print("Original tree:", original)
    if expected is not None:
        print("Expected      :", expected)
    print("Actual        :", actual)
    print()

def print_tree_state(tree, label):
    print(f"{label} (in-order): {[node for node in tree]}")
    print
if __name__ == "__main__":

    print("\n==== Manual Tests for LazyBinarySearchTree ====\n")

    # Test 1: Insert Nodes
    tree = LazyBinarySearchTree([10, 5, 15])
    original = [node for node in tree]
    show_test("Test 1a: Initial tree (in-order traversal)", "[5, 10, 15]", original)
    print_tree_state(tree, "Initial Tree Structure")

    tree.insert(7)
    show_test("Test 1b: Tree after inserting 7", "[5, 7, 10, 15]", [node for node in tree], original)
    print_tree_state(tree, "Tree After Insert 7")

    # Test 2: Remove Node
    original = [node for node in tree]
    tree.remove(5)
    show_test("Test 2: Tree after removing 5", "[7, 10, 15]", [node for node in tree], original)
    print_tree_state(tree, "Tree After Logical Deletion of 5")

    # Test 3: Reinsert Deleted Node
    original = [node for node in tree]
    tree.insert(5)
    show_test("Test 3: Tree after reinserting 5", "[5, 7, 10, 15]", [node for node in tree], original)
    print_tree_state(tree, "Tree After Reinserting 5")

    # Test 4: Garbage Collection
    print("=" * 40)
    print("Test 4: Garbage Collection")
    tree = LazyBinarySearchTree([10, 5, 15])
    print_tree_state(tree, "Initial Tree")

    tree.remove(5)
    print_tree_state(tree, "After Logical Deletion of 5")

    tree.collect_garbage()
    print_tree_state(tree, "After Garbage Collection")

    # Test 5: Remove from Empty Tree
    empty_tree = LazyBinarySearchTree()
    print("=" * 40)
    print("Test 5: Remove from Empty Tree")
    print_tree_state(empty_tree, "Initial Empty Tree")
    try:
        empty_tree.remove(10)
    except Exception as e:
        print("Expected error when removing from empty tree:")
        print(f"Exception: {e}\n")

    # Test 6: Logical Deletion Check
    tree = LazyBinarySearchTree([20, 10, 30, 5, 15, 25, 35])
    tree.remove(10)
    tree.remove(30)
    print("=" * 40)
    print("Test 6: Logical Deletion Check")
    print_tree_state(tree, "Tree with Logical Deletions")
    print("Membership checks:")
    print(f"10 in tree? {'yes' if 10 in tree else 'no'}")
    print(f"30 in tree? {'yes' if 30 in tree else 'no'}")
    print(f"25 in tree? {'yes' if 25 in tree else 'no'}\n")

    # Test 7: Garbage Collection Impact
    print("=" * 40)
    print("Test 7: Garbage Collection on Tree with Deletions")
    print_tree_state(tree, "Before Garbage Collection")
    tree.collect_garbage()
    print_tree_state(tree, "After Garbage Collection")

    # Test 8: Physical vs Logical Size
    print("=" * 40)
    print("Test 8: Size Comparisons")
    print(f"Logical size (non-deleted nodes): {len([x for x in tree])}")
    print(f"Physical size (total nodes in tree): {tree.size_physical}")