''''Modul contains implementation of Huffman Compression algorithm.'''

import sys
import warnings
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
        '''Print branch of the node in breath first fession into list.'''
        queue = deque()
        queue.appendleft(self)
        visit_list = [self]

        while len(queue):
            node = queue.pop()
            visit_list.extend((node.left, node.right))

            if node.left:
                queue.appendleft(node.left)

            if node.right:
                queue.appendleft(node.right)

        return visit_list


class HuffmanCompressor:
    '''Huffman string compression implementation.

    Attributes:
        string(str): String to encode and build Huffman tree.

    Methods:
        encode(): Encode string to binary representation
        decode(string): Decode Huffman binary representation back to string.
    '''
    def __init__(self, string):
        assert isinstance(string, str) and string, \
        'Argument needs to be a not empty string.'

        self.string = string
        self._root = self._build_hf_tree()
        self._encode_map = self._get_encode_map()

    def _build_hf_tree(self):
        counter = [Node((count, char))
                   for char, count in Counter(self.string).items()]

        heapq.heapify(counter)
        heap = counter

        # edge case of one character:
        if len(heap) == 1:
            count = heap[0][0]
            root = Node((count, ''))
            root.left = heap[0]
            return root

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

        root = heap[0]
        return root

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

    def decode(self, bin_str=None, error='raise'):
        '''Returns string representation of huffman binary code.

        Args:
            bin_str(string): Huffman encoded string in binary code. Optional,
                string attribute used if not provided.
            errors(string): Error handling and encoding sum check.
                'ignore': Ignores sum check error and strips last bits which
                    does not represent any character in encoded_map
                'warn': As ignore, but raises warning.
                'raise': Raises attribute exception

        '''
        bin_str = bin_str if bin_str else self.encode()

        decoded_str = ''
        bit_idx = 0
        node = self._root
        while bit_idx < len(bin_str):
            prev_node = node

            # traverse Huffman tree
            if bin_str[bit_idx] == '0':
                node = node.left
            elif bin_str[bit_idx] == '1':
                node = node.right
            else:
                raise AssertionError('bin_str needs to be binary sequence.')

            # Update decoded string and increase bit index
            if node:
                char = node[1]
                if char:
                    decoded_str += char
                bit_idx += 1

            # Jump back to root
            else:
                # Prevent infinite loop for example decode
                # '1' with Huffmant tree [(7, ''), (7, 'A'), None]
                # or '0' with [(7, ''), None, (7, 'A')]
                if prev_node is self._root:
                    self._check_sum(node, 'raise')
                else:
                    node = self._root

        # Check sum test
        last_node = node
        self._check_sum(last_node, error)

        return decoded_str

    def _check_sum(self, node, error):
        '''Checks whether node is leaf node of Huffman Tree and raises
        exception, warning or passes.
        '''
        if not (node and node[1]):

            err_msg = 'Sum check of binary string failed. '
            if error == 'ignore':
                pass
            elif error == 'warn':
                warnings.warn(
                    err_msg + 'Last non matched binary sequence stripped.')
            elif error == 'raise':
                raise AssertionError(err_msg)
            else:
                raise NotImplementedError()


if __name__ == "__main__":
    codes = {}

    a_great_sentence = "The bird is the word"

    print ("The size of the data is: {}\n".format(sys.getsizeof(a_great_sentence)))
    print ("The content of the data is: {}\n".format(a_great_sentence))

    hc = HuffmanCompressor(a_great_sentence)
    encoded_data = hc.encode()
    # encoded_data, tree = huffman_encoding(a_great_sentence)

    print ("The size of the encoded data is: {}\n".format(sys.getsizeof(int(encoded_data, base=2))))
    print ("The content of the encoded data is: {}\n".format(encoded_data))

    decoded_data = hc.decode(encoded_data)

    print ("The size of the decoded data is: {}\n".format(sys.getsizeof(decoded_data)))
    print ("The content of the encoded data is: {}\n".format(decoded_data))
