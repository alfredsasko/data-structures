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
