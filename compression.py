''''Modul contains implementation of Huffman Compression algorithm.'''

import sys
import heapq
from collections import deque
from collections import Counter


class Node(tuple):
    '''Extends tuple class by left and right child attributes, while node value
    is stored as tuple. Includes to_list method to tranfrom tree structure to
    list using breath first search method.'''

    def __new__(cls, sequence):
        return super(Node, cls).__new__(cls, sequence)

    def __init__(self, sequence):
        self.left = None
        self.right = None

    def to_list(self):
        queue = deque()
        queue.appendleft(self)
        visit_list = []

        while len(queue):
            node = queue.pop()
            visit_list.append(node)

            if node.left:
                queue.appendleft(node.left)

            if node.right:
                queue.appendleft(node.right)

        return visit_list


class HuffmanCompressor:
    '''Huffman string compression implementation.

    Attributes:
        string(str): String which needs to be compressed.

    Methods:
        encode(): Encode string to binary representation
        decode(string): Decode binary representation back to string.
    '''
    def __init__(self, string):
        assert isinstance(string, str) and string, \
        'Argument needs to be a not empty string.'

        self.string = string
        self._root = self._get_root()
        self._encode_map = self._get_encode_map()

    def _get_root(self):
        '''Builds Huffman tree.'''
        counter = [Node((count, char))
                   for char, count in Counter(self.string).items()]

        heapq.heapify(counter)
        heap = counter
        while len(heap) >= 2:
            node1, node2 = heapq.heappop(heap), heapq.heappop(heap)
            new_node = Node((node1[0] + node2[0], ''))

            if node1 <= node2:
                new_node.left = node1
                new_node.right = node2
            else:
                new_node.left = node2
                new_node.right = node1

            heapq.heappush(heap, new_node)

        return heap[0]

    def _get_encode_map(self):
        '''Builds Huffman mapping of characters to binary codes'''
        return self._get_bin_code(self._root, [], {})

    def _get_bin_code(self, node, bin_code, bin_dict):

        if (not node.left) and (not node.right):
            char = node[1]
            if char:
                if node is self._root:
                    bin_dict[char] = '0'
                else:
                    bin_dict[char] = ''.join(bin_code)
            else:
                raise AttributeError(
                    'The leaf node needs to be valid charater node')

        if node.left:
            left_code = bin_code.copy()
            left_code.append('0')
            bin_dict = self._get_bin_code(node.left, left_code, bin_dict)

        if node.right:
            right_code = bin_code.copy()
            right_code.append('1')
            bin_dict = self._get_bin_code(node.right, right_code, bin_dict)

        return bin_dict

    def encode(self):
        '''Returns Huffman binary code representation of the string.'''
        bin_str = ''.join([self._encode_map[char] for char in self.string])
        return bin_str

    def decode(bin_str):
        pass




def huffman_encoding(data):
    pass

def huffman_decoding(data,tree):
    pass

if __name__ == "__main__":
    codes = {}

    a_great_sentence = "The bird is the word"

    print ("The size of the data is: {}\n".format(sys.getsizeof(a_great_sentence)))
    print ("The content of the data is: {}\n".format(a_great_sentence))

    encoded_data, tree = huffman_encoding(a_great_sentence)

    print ("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
    print ("The content of the encoded data is: {}\n".format(encoded_data))

    decoded_data = huffman_decoding(encoded_data, tree)

    print ("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
    print ("The content of the encoded data is: {}\n".format(decoded_data))
