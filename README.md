# Lazy-Delete Binary Search Tree

## Overview
This project implements a Binary Search Tree (BST) in Python using lazy deletion, where nodes are marked as deleted instead of being immediately removed. This approach improves performance for frequent insert/delete operations.

## Features
- Lazy deletion (logical removal of nodes)
- Node reactivation on reinsertion
- Garbage collection to physically remove deleted nodes
- Accurate tracking of logical vs physical tree size
- Unit tests covering core functionality

## How It Works
- Deletions mark nodes as inactive instead of removing them
- Re-inserting a deleted value reactivates the node
- A cleanup process removes all logically deleted nodes when needed

## Example Usage
bst.insert(10)
bst.insert(5)
bst.delete(5)        # marks node as deleted
bst.insert(5)        # reactivates node
bst.cleanup()        # physically removes deleted nodes

## Running Tests
python -m unittest discover

## Purpose
This project demonstrates understanding of data structures, optimization tradeoffs, and handling logical vs physical state in systems.
