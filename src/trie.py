class Node:
    def __init__(self, payload=None):
        self.children = {}
        self.isFinal = False
        self.payload = payload

class Trie:
    def __init__(self):
        # root node
        self.root = Node()

    def insert(self, key, payload):
        curr_node = self.root

        for char in key:
            # If a character is not found, create a new node in the trie
            if char not in curr_node.children:
                curr_node.children[char] = Node()
            curr_node = curr_node.children[char]

        # Leaf node
        curr_node.payload = payload
        curr_node.isFinal = True
        return

    def delete(self, key):
        curr_node = self.root

        for char in key:
            # If a character is not found, create a new node in the trie
            if char not in curr_node.children:
                return False
            curr_node = curr_node.children[char]

        # Clear children of high-level key
        curr_node.children.clear()
        curr_node.payload = None
        curr_node.isFinal = False
        return True

    # Search key in the trie
    def search(self, key):
        curr_node = self.root

        for char in key:
            if char in curr_node.children:
                curr_node = curr_node.children[char]
            else:
                return [False, None]

        return [curr_node != None and curr_node.isFinal, curr_node.payload]
