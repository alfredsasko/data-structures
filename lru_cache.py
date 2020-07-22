from collections import deque

class LRU_Cache(object):
    '''Least recently used cache class.

    Attributes:
        capacity: Positive integer, capacity of the cache memory
        memory: Dictionary, hash map storing key-value pairs
        lru: Key of the least recently used key-value pair in cache

    Methods:
        put(key1, value1, ... [key_value_pairs]):
            Inserts the key-value pair in cache
        get(key1, .... [key_array_like])
            Returns the value from the cache, None if key does not exists
    '''

    def __init__(self, capacity=5):
        # Initialize class variables
        assert isinstance(capacity, int) and (capacity > 0), \
            'Capacity needs to be positive int.'

        self.capacity = capacity
        self.memory = dict()
        self._lru = deque()

    def get(self, key):
        'Retrieve item from provided key. Return None if nonexistent.'
        try:
            return self.memory[key]
        except KeyError:
            return None

    def set(self, key, value):
        '''Set the value if the key is not present in the cache
        If the cache is at capacity remove the oldest item.
        '''
        self.memory[key] = value
        self._lru.appendleft(key)

        if len(self.memory) > self.capacity:
            del self.memory[self._lru.pop()]
