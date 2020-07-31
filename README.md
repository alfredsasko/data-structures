# Data Structures
This project shows solutions of various data structure problems the Data Scientist or Software Engineer can be asked during the technical interview. It includes design choices as well as complexity analysis.

## 1. Least Recently Used Cache

### 1.1. Problem Description
Caching can be defined as the process of storing data into a temporary data storage to avoid re-computation or to avoid reading the data from a relatively slower part of memory again and again. Thus caching serves as a fast "look-up" storage allowing programs to execute faster.

The lookup operation (i.e., `get()`) and `put()` / `set()` is supposed to be fast for a cache memory.

While doing the `get()` operation, if the entry is found in the cache, it is known as a cache hit. If, however, the entry is not found, it is known as a cache miss.

When designing a cache, we also place an upper bound on the size of the cache. If the cache is full and we want to add a new entry to the cache, we use some criteria to remove an element. After removing an element, we use the put() operation to insert the new element. The remove operation should also be fast.

For our first problem, the goal will be to design a data structure known as a Least Recently Used (LRU) cache. An LRU cache is a type of cache in which we remove the least recently used entry when the cache memory reaches its limit. For the current problem, consider both get and set operations as an use operation.

Your job is to use an appropriate data structure(s) to implement the cache.

In case of a cache hit, your `get()` operation should return the appropriate value.
In case of a cache miss, your `get()` should return -1.
While putting an element in the cache, your `put()` / `set()` operation must insert the element. If the cache is full, you must write code that removes the least recently used entry first and then insert the element.
All operations must take O(1) time.

For the current problem, you can consider the size of cache = 5.

### 1.2. Design Choices
Cash is used to access elements very frequently. So it is imperative that these operations have constant time complexity. The Python dictionary can be used for this purpose.

Keeping a track of least recently used element can be efficiently done with FIFO data structure. The Python Deque can be used for this purpose (List is also possible but is less efficient)

### 1.3. Time Complexity
#### Method `Cache.set()`
```
def set(self, key, value):
    '''Set the value if the key is not present in the cache
    If the cache is at capacity remove the oldest item.
    '''
    self.memory[key] = value
    self._lru.appendleft(key)

    if len(self.memory) > self.capacity:
        del self.memory[self._lru.pop()]
```
| Command                	| Time Complexity 	|
|------------------------	|:---------------:	|
| dict.\_\_getitem\_\_() 	|       O(1)      	|
| deque.appendleft()     	|       O(1)      	|
| dict.\_\_len\_\_()     	|       O(1)      	|
| Worst Total            	|       O(1)      	|

## Method `Cache.get()`
```
def get(self, key):
    'Retrieve item from provided key. Return None if nonexistent.'
    try:
        return self.memory[key]
    except KeyError:
        return None
```
| Command                	| Time Complexity 	|
|------------------------	|:---------------:	|
| dict.\_\_getitem\_\_() 	|       O(1)      	|
| Worst Total            	|       O(1)      	|

## 2. Finding Files

### 2.1. Problem Description
For this problem, the goal is to write code for finding all files under a directory (and all directories beneath it) that end with ".c"

Here is an example of a test directory listing, which can be downloaded [here](https://s3.amazonaws.com/udacity-dsand/testdir.zip)

```
./testdir
./testdir/subdir1
./testdir/subdir1/a.c
./testdir/subdir1/a.h
./testdir/subdir2
./testdir/subdir2/.gitkeep
./testdir/subdir3
./testdir/subdir3/subsubdir1
./testdir/subdir3/subsubdir1/b.c
./testdir/subdir3/subsubdir1/b.h
./testdir/subdir4
./testdir/subdir4/.gitkeep
./testdir/subdir5
./testdir/subdir5/a.c
./testdir/subdir5/a.h
./testdir/t1.c
./testdir/t1.h
```

Python's os module will be useful—in particular, you may want to use the following resources:

 - [`os.path.isdir(path)`](https://docs.python.org/3.7/library/os.path.html#os.path.isdir)
 - [`os.path.isfile(path)`](https://docs.python.org/3.7/library/os.path.html#os.path.isfile)
 - [`os.listdir(directory)`](https://docs.python.org/3.7/library/os.html#os.listdir)
 - [`os.path.join(…)`](https://docs.python.org/3.7/library/os.path.html#os.path.join)

Note: `os.walk()` is a handy Python method which can achieve this task very easily. However, for this problem you are not allowed to use `os.walk()`.

### 2.2. Design Choices
`FileManager` class will be designed to handle the task in question. The simple for loop will be used to retrieve the list of filenames and list of child directories. The queue will be used to handle the concurrent processing  using threads to reduce execution time and aggregate file list from whole directory tree.

### 2.3. Time Complexity
As all the files need to be searched to retrieve the ones matching the request, the worst time complexity is O(n C^k). As directory tree structure in the file system can be huge and demanding regarding I/O operations the concurrency using threads will be applied to reduce execution time O(n C^k / t), where t is number of threads. The time complexity of the searching algorithm stays the same O(n).

#### Method `FileManager.find_files()`
```
def _find_files(self, path, query, regex=False):
    '''Returns list of querying files in specified directory (path) and
    list of child directories. Method is used for internal purposes and is
    wrapped into multi-threading interface to return files from whole
    directory tree.
    '''

    assert isinstance(query, str), 'Query needs to be string.'
    assert isinstance(path, (str, pathlib.Path)), \
    'Path needs to be str or pathlib.Path object.'

    path = pathlib.Path(path) if isinstance(path, str) else path

    assert path.is_dir(), 'Directory not found in {}'.format(os.getcwd())

    if regex:
        query = re.compile(query)

    subdirs, files = [], []
    for p in path.iterdir():

        if p.is_dir() and not p.is_symlink():
            subdirs.append(p)

        if p.is_file():
            file_path = p.as_posix()

            if ((regex and query.match(file_path))
                or ((not regex) and (query in file_path))):

                files.append(file_path)

    return subdirs, files
```

| Command              	| Time Complexity 	|
|----------------------	|:---------------:	|
| path.iterdir()       	|      O(n)     	|
| &nbsp;&nbsp;&nbsp;&nbsp;query.match()    	|     O(C^k)    	|
| &nbsp;&nbsp;&nbsp;&nbsp;str.\_\_contains\_\_() 	|      O(s)     	|
| Worst Total          	|    O(n C^k)   	|

- n - number of directories and file in directory tree
- k - length of regular expression
- C - regular expression alternations
- s - length of the string

## 3. Huffman Coding

### 3.1. Problem Description
#### 3.1.1. Overview - Data Compression
In general, a data compression algorithm reduces the amount of memory (bits) required to represent a message (data). The compressed data, in turn, helps to reduce the transmission time from a sender to receiver. The sender encodes the data, and the receiver decodes the encoded data. As part of this problem, you have to implement the logic for both encoding and decoding.

A data compression algorithm could be either __lossy__ or __lossless__, meaning that when compressing the data, there is a loss (lossy) or no loss (lossless) of information. The __Huffman Coding__ is a lossless data compression algorithm. Let us understand the two phases - encoding and decoding with the help of an example.

#### 3.1.2. Huffman Encoding
Assume that we have a string message `AAAAAAABBBCCCCCCCDDEEEEEE` comprising of 25 characters to be encoded. The string message can be an unsorted one as well. We will have two phases in encoding - building the Huffman tree (a binary tree), and generating the encoded data. The following steps illustrate the Huffman encoding:

##### 3.1.2.1 Build the Huffman Tree
A Huffman tree is built in a bottom-up approach.

###### Step 1
First, determine the frequency of each character in the message. In our example, the following table presents the frequency of each character.

| Unique Character 	| Frequency 	|
|:----------------:	|:---------:	|
|         A        	|     7     	|
|         B        	|     3     	|
|         C        	|     7     	|
|         D        	|     2     	|
|         E        	|     6     	|

###### Step 2
Each row in the table above can be represented as a node having a character, frequency, left child, and right child. In the next step, we will repeatedly require to pop-out the node having the lowest frequency. Therefore, build and sort a list of nodes in the order lowest to highest frequencies. Remember that a list preserves the order of elements in which they are appended.

We would need our list to work as a [priority queue](https://en.wikipedia.org/wiki/Priority_queue), where a node that has lower frequency should have a higher priority to be popped-out. The following snapshot will help you visualize the example considered above:

</div>
<div style="overflow: hidden; padding: 20px 0px">
    <img src="/assets/01_priority_queue.png" style="float: left; width: 100%;"/>
</div>

Can you come up with other data structures to create a priority queue? How about using a min-heap instead of a list? You are free to choose from anyone.

###### Step 3
Pop-out two nodes with the minimum frequency from the priority queue created in the above step.

###### Step 4
Create a new node with a frequency equal to the sum of the two nodes picked in the above step. This new node would become an internal node in the Huffman tree, and the two nodes would become the children. The lower frequency node becomes a left child, and the higher frequency node becomes the right child. Reinsert the newly created node back into the priority queue.

Do you think that this reinsertion requires the sorting of priority queue again? If yes, then a min-heap could be a better choice due to the lower complexity of sorting the elements, every time there is an insertion.

###### Step 5
Repeat steps 3 and 4 until there is a single element left in the priority queue. The snapshots below present the building of a Huffman tree.

</div>
<div style="overflow: hidden; padding: 20px 0px">
    <img src="/assets/02_building_huffman_tree.png" style="float: left; width: 100%;"/>
</div>

</div>
<div style="overflow: hidden; padding: 20px 0px">
    <img src="/assets/03_building_huffman_tree.png" style="float: left; width: 100%;"/>
</div>

###### Step 6
For each node, in the Huffman tree, assign a bit 0 for left child and a 1 for right child. See the final Huffman tree for our example:

<div style="overflow: hidden; padding: 20px 0px">
    <img src="/assets/04_building_huffman_tree.png" style="float: left; width: 100%;"/>
</div>

##### 3.1.2.2 Generate the Encoded Data
###### Step 7
Based on the Huffman tree, generate unique binary code for each character of our string message. For this purpose, you'd have to traverse the path from root to the leaf node.

| Unique Character 	| Frequency 	| Huffman Code 	|
|:----------------:	|:---------:	|:------------:	|
|         D        	|     2     	|      000     	|
|         B        	|     3     	|      001     	|
|         E        	|     6     	|      01      	|
|         A        	|     7     	|      10      	|
|         C        	|     7     	|      11      	|

__Points to Notice__

 - Notice that the whole code for any character is not a prefix of any other code. Hence, the Huffman code is called a [Prefix code](https://en.wikipedia.org/wiki/Prefix_code).
 - Notice that the binary code is shorter for the more frequent character, and vice-versa.
 - The Huffman code is generated in such a way that the entire string message would now require a much lesser amount of memory in binary form.
 - Notice that each node present in the original priority queue has become a leaf node in the final Huffman tree.

This way, our encoded data would be `1010101010101000100100111111111111111000000010101010101`

#### 3.1.3. Huffman Decoding
Once we have the encoded data, and the (pointer to the root of) Huffman tree, we can easily decode the encoded data using the following steps:

 1. Declare a blank decoded string
 2. Pick a bit from the encoded data, traversing from left to right.
 3. Start traversing the Huffman tree from the root.

   - If the current bit of encoded data is `0`, move to the left child, else move to the right child of the tree if the current bit is `1`.
   - If a leaf node is encountered, append the (alphabetical) character of the leaf node to the decoded string.


 4. Repeat steps #2 and #3 until the encoded data is completely traversed.

You will have to implement the logic for both encoding and decoding in the following template. Also, you will need to create the sizing schemas to present a summary.

#### 3.1.4 Visualization Resource
Check this website to visualize the Huffman encoding for any string message - [Huffman Visualization](https://people.ok.ubc.ca/ylucet/DS/Huffman.html)

### 3.2. Design Choices
`HuffmanCompressor` class will be designed to implement Huffman encoding and decoding functions. Building the Huffman tree requires searching for minimum frequency items and frequent sorting. The __min heap__ structure is best for this purpose with time complexity O(1) for `peek()` operation and O(log n) for `push()` and `pop()` operation. The python already implement min heap in its `heapq` library.

The encoding table is build up by depth first search algorithm. `encode()` method will use it to get character binary codes. It will be stored as hash-table - dictionary implementation in python, where time complexity for get and set method is O(1).

`decode` method will traverse Huffman tree with search sequence determined by binary code of encoded string with time complexity of O(k n), where n is number of bits in encoded string and k is number of characters in Huffman encode table.

The reason for k is that implementation is using while loop where bit index is only increased if current node has child nodes. For situations where algorithm hits leaf the index stays constant only pointer jumps to root to search for next character. For the length of string going to infinity, with relatively small encode table we can generalize to O(n).

### 3.3. Time Complexity

#### Method `HuffmanCompressor.encode()`
```
def encode(self):
    '''Returns Huffman binary code representation of the string.'''
    bin_str = ''.join([self._encode_map[char] for char in self.string])
    return bin_str

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

    # Depth First Search builds the Huffman encoding dictionary
    if node.left:
        left_code = bin_code.copy()
        left_code.append('0')
        bin_dict = self._get_bin_code(node.left, left_code, bin_dict)

    if node.right:
        right_code = bin_code.copy()
        right_code.append('1')
        bin_dict = self._get_bin_code(node.right, right_code, bin_dict)

    return bin_dict
```

| Command              	| Time Complexity 	|
|----------------------	|:---------------:	|
| self._get_bin_code() 	|       O(n)      	|
| Worst Total          	|       O(n)      	|

#### Method `HuffmanCompressor.decode()`
```
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
```
| Command              	| Time Complexity 	|
|----------------------	|:---------------:	|
| while loop          	|   O(n k)         	|
| Worst Total          	|   O(n)          	|

 - n - number of characters in string
 - k - number of characters in Huffman encode table

## 4. Active Directory

### 4.1. Problem Description
In Windows Active Directory, a group can consist of user(s) and group(s) themselves. We can construct this hierarchy as such. Where User is represented by str representing their ids.

```
class Group(object):
    def __init__(self, _name):
        self.name = _name
        self.groups = []
        self.users = []

    def add_group(self, group):
        self.groups.append(group)

    def add_user(self, user):
        self.users.append(user)

    def get_groups(self):
        return self.groups

    def get_users(self):
        return self.users

    def get_name(self):
        return self.name


parent = Group("parent")
child = Group("child")
sub_child = Group("subchild")

sub_child_user = "sub_child_user"
sub_child.add_user(sub_child_user)

child.add_group(sub_child)
parent.add_group(child)
````

Write a function that provides an efficient look up of whether the user is in a group.

```
def is_user_in_group(user, group):
    """
    Return True if user is in the group, False otherwise.

    Args:
      user(str): user name/id
      group(class:Group): group to check user membership against
    """
    return None
```

### 4.2. Design Choices
The `is_user_in_group()` function has been embedded into `Group` class by overwriting `object.__contains__()` method using inheritance. This special internal method enables using in operator to check if user is in the `Group` class in form of `user in group`.

The `Group.__contains__()` is recursive or operator checking the user membership in current group users and its all children. One's the first match is found it stops execution of the recursion. The worst case time complexity is O(n) where n is the number of users listed in group hierarchy with duplicates included.

### 4.3. Time complexity
#### Method `Group.__contains__()`
```
def __contains__(self, user):
    return ((user in self.users)
            or any(group.__contains__(user) for group in self.groups))
```
| Command             	| Time Complexity 	|
|---------------------	|:---------------:	|
| list.__contains__() 	|       O(k)      	|
| Worst Total         	|       O(n)      	|

 - k - number of users in the Group
 - n - number of users in Group hierarchy, including duplicates

## 5. Block-chain

### 5.1. Problem Description
A [Blockchain](https://en.wikipedia.org/wiki/Blockchain) is a sequential chain of records, similar to a linked list. Each block contains some information and how it is connected related to the other blocks in the chain. Each block contains a cryptographic hash of the previous block, a timestamp, and transaction data. For our blockchain we will be using a [SHA-256](https://en.wikipedia.org/wiki/SHA-2) hash, the [Greenwich Mean Time](https://en.wikipedia.org/wiki/Greenwich_Mean_Time) when the block was created, and text strings as the data.

Use your knowledge of linked lists and hashing to create a block-chain implementation.
<div style="overflow: hidden; padding: 20px 0px">
    <img src="/assets/05_blockchain.png" style="float: left; width: 100%;"/>
</div>

We can break the block-chain down into three main parts. First is the information hash:
```
import hashlib

def calc_hash(self):
      sha = hashlib.sha256()

      hash_str = "We are going to encode this string of data!".encode('utf-8')

      sha.update(hash_str)

      return sha.hexdigest()
```

We do this for the information we want to store in the block chain such as transaction time, data, and information like the previous chain. The next main component is the block on the block-chain:
```
class Block:

    def __init__(self, timestamp, data, previous_hash):
      self.timestamp = timestamp
      self.data = data
      self.previous_hash = previous_hash
      self.hash = self.calc_hash()
```

Above is an example of attributes you could find in a `Block` class.

Finally you need to link all of this together in a block chain, which you will be doing by implementing it in a linked list. All of this will help you build up to a simple but full block-chain implementation!
