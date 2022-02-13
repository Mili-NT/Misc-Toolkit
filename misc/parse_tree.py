#!/usr/bin/env python3
import sys
import time
import regex # This library allows for more functionality than re
from pathlib import PurePath, Path

"""
This parses the output of a windows tree command into their absolute paths.
The code is bad, the regex is good, the tree class is silly.

No one's gonna use this so who cares.
"""

class Tree:
    def __init__(self, root):
        self.path = root
        self.height = 0
        self.file_count = 0
        self.dir_count = 0
        self.children = []
        self.paths = []

    def new_node(self,node_obj):
        self.children.append(node_obj)
    def get_path(self):
        return str(self.path)
    def output(self):
        for child in self.children:
            if child.node_type == "file":
                self.file_count += 1
            else:
                self.dir_count += 1
            self.paths.append(child.get_path())
            if child.children:
                child.get_children(self)
        with open("ParsedTree.txt", "w") as f:
            for path in self.paths:
                f.write(f"{path}\n")
    def get_nodes_info(self):
        # File Count & Dir Count
        print(f"File Nodes: {self.file_count}\nDirectory Nodes: {self.dir_count}\n")
class Node:
    def __init__(self, path, height, parent, node_type):
        self.parent = parent
        self.path = PurePath.joinpath(self.parent.path, path)
        self.node_type = node_type
        self.height = height
        self.children = []

    def new_node(self,node_obj):
        node_obj.set_parent(self)
        self.children.append(node_obj)
    def set_parent(self, parent):
        self.parent = parent
    def get_parent(self):
        return self.parent
    def get_path(self):
        return str(self.path)
    def get_children(self, tree):
        for child in self.children:
            if child.node_type == "file":
                tree.file_count += 1
            else:
                tree.dir_count += 1
            if child.children:
                child.get_children(tree)
                tree.paths.append(child.get_path())
            else:
                tree.paths.append(child.get_path())

def parse_windows_tree(filepath):
    with open(filepath, 'r') as f:
        lines = [line for line in f.readlines() if not regex.match(r"^[| ]+$", line)]
        file_tree = Tree(PurePath(lines[0].rstrip()))
        current_parent = file_tree
        lines = lines[1:]
        for index,line in enumerate(lines):
            next_line = lines[index+1] if index+1<len(lines) else line
            height = len(regex.match(r"(^[\||\+|\\| ]{1}[ |\||\\|-]*)", line).group())//4
            next_height = len(regex.match(r"(^[\||\+|\\| ]{1}[ |\||\\|-]*)", next_line).group())//4
            file = regex.match(r"([ |\|]+[\|| ]+)([^+|\\|\n]+[^ |\n]$)", line)
            directory = regex.match(r"(^.*?[+|\\]-{3})(.*$)", line)
            if file:
                node = Node(file.groups()[1], height, current_parent, "file")
                current_parent.new_node(node)
            if directory:
                node = Node(directory.groups()[1], height, current_parent, "dir")
                current_parent.new_node(node)
                current_parent = node
            if next_height < height:
                while current_parent.height >= next_height:
                    current_parent = current_parent.parent
    return file_tree

def main():
    filepath = sys.argv[1] if len(sys.argv) > 1 else None
    while filepath is None or not Path.is_file(filepath):
        filepath = Path(input(f"Enter the path to the tree output: "))
        print(filepath)
    start_time = time.time()
    print(f"Parsing File...\n")
    parsed_tree = parse_windows_tree(filepath)
    parsed_tree.output()
    parsed_tree.get_nodes_info()
    print(f"Parsing runtime: {time.time() - start_time}")

if __name__ == '__main__':
    main()
