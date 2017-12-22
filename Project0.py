"""
Project 0
William Groble
CMPS 2200
11/2/2017
"""

class Node(object):
    """Initialize a node."""

    def __init__(self, data=[], root=True, child=[]):
        """Initialize node that defaults to an empty root with no children."""
        self.data = data
        self.children = child
        self.root = root

    def setChild(self, child=[]):
        """Helper method to set a node a specified child."""
        for x in child:
            x.root = False
        self.children = child
        return

    def removeChild(self, child):
        """Helper method to remove specified child from node."""
        self.children.remove(child)
        return

class Tree(object):
    """Initialize the tree, and specifies the minimum degrees."""

    def __init__(self, data, nodes=[], degrees=2):
        """Initialize B tree with min degrees specified."""
        self.nodes = nodes
        self.degrees = degrees
        self.root = Node([data])

    def insert(self, key):
        """Inserts a Node into a tree, first step in insert"""
        if (len(self.root.data) == ((2*self.degrees)-1)):
            # insert new root node if the current root node is full
            r = self.root
            self.root = Node()
            self.root.setChild([r])
            self.root.data = [] # I have no idea why this needs to be here but it just does
            # Split old root to be 2 children of new root s
            self.splitChild(self.root, r, key)
            self.insertNonfull(self.root, key)
        else:
            self.insertNonfull(self.root, key)

    def insertNonfull(self, root, key):
        """Inserts an element into a nonfull node"""
        if (root.children == []):
            root.data.extend([key])
            root.data.sort()
        else:
            #c = set child of x whose subtree should contain key
            c = None
            for x in root.children:
                for y in x.data:
                    if key < y:
                        c = x
                        break
            if c == None:
                c = root.children[-1]
        
            if len(c.data) == ((2*self.degrees)-1):
                self.splitChild(root, c, key)
                for x in root.children:
                    for y in x.data:
                        if key < y:
                            c = x
                            break
                    c = root.children[-1]
            # c = child of x whose subtree contains key
            self.insertNonfull(c, key)

    def splitChild(self, node, child, key):
        """Splits a node into to chidren and assigns the new children the original childs children"""
        child1 = Node([child.data[0]], False)
        child2 = Node([child.data[2]], False)
        if child.children:
            child1.setChild(child.children[:int((len(child.children)/2))])
            child2.setChild(child.children[int((len(child.children)/2)):])
        pushVal = child.data[1]
        node.removeChild(child)
        li = []
        for x in node.children:
            li.extend([x])
        li.extend([child1, child2])
        node.setChild(li)
        node.data.extend([pushVal])
        node.data.sort()

    

    def search(self, key, root):
        """Iterate through each node to compare to key value being searched for"""
        i = 0;
        while(len(root.data) > i) and (root.data[i] < key):
            i = i+1
        if (len(root.data) > i) and (root.data[i] == key):
            return True
        if (root.children == []):
            return False
        else:
            return self.search(key, root.children[i])

    def print_tree(self):
        """Print an level-order representation."""
        crrnt = [self.root]
        while crrnt:
            next = []
            out = ""
            for node in crrnt:
                if node.children:
                    next.extend(node.children)
                out += str(node.data) + " "
            print(out)
            crrnt = next

def main():
    # Hardcoded Tree
    a = Node([2, 4], False)
    b = Node([11], False)
    c = Node([1], False)
    d = Node([3], False)
    e = Node([5, 6, 7], False)
    f = Node([9, 10], False)
    g = Node([12], False)

    a.setChild([c, d, e])
    b.setChild([f, g])
    tree1 = Tree(8, [a, b, c, d, e, f, g])
    tree1.root.setChild([a, b])
    tree1.print_tree()
    print "\n"
    
    # Tree that is initially 1 root node and the rest of the values are inserted (currently up to 25)
    tree2 = Tree(1)
    for x in range(2,16):
        tree2.insert(x)

    tree2.print_tree()
    print tree2.search(10, tree2.root)  # should return True
    print tree2.search(25, tree2.root)  # should return False

if __name__ == '__main__':
    main()
