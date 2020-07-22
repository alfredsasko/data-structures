'''Modul contains test methods for LRU_Cache class'''

import pytest
from lru_cache import LRU_Cache


class TestCache:

    def test_init_method(self, cache, standard_capacity):
        assert ((len(cache.memory) == 0)
                and (len(cache._lru) == 0)
                and (cache.capacity == standard_capacity))

    def test_init_method_valid_args(self, valid_capacity):
        cache = LRU_Cache(valid_capacity)
        assert cache.capacity == valid_capacity

    def test_init_method_invalid_args(self, invalid_capacity):
        with pytest.raises(AssertionError):
            chash = LRU_Cache(invalid_capacity)

    def test_set_method_args(self, cache, key, value):
        cache_size = len(cache.memory)
        cache.set(key, value)
        assert ((cache.memory[key] == value)
                and (len(cache.memory) == cache_size + 1))

    def test_set_method_over_capacity(self, full_capacity_cache):
        new_key, new_value, rlu_key, rlu_value, cache = full_capacity_cache
        cache.set(new_key, new_value)
        assert ((cache.memory[new_key] == new_value)
                and (rlu_key not in cache.memory)
                and (len(cache.memory) == cache.capacity))

    def test_set_method_valid_key(self, full_capacity_cache):
        _, _, in_key, in_value, cache = full_capacity_cache
        assert cache.get(in_key) == in_value

    def test_set_method_invalid_key(self, full_capacity_cache):
        new_key, _, _, _, cache = full_capacity_cache
        assert not cache.get(new_key)

# cachee = LRU_Cache(5)
#
# cachee.set(1, 1);
# cachee.set(2, 2);
# cachee.set(3, 3);
# cachee.set(4, 4);
#
#
# cachee.get(1)       # returns 1
# cachee.get(2)       # returns 2
# cachee.get(9)      # returns -1 because 9 is not present in the cache
#
# cachee.set(5, 5)
# cachee.set(6, 6)
#
# cachee.get(3)      # returns -1 because the cache reached it's capacity and 3 was the least recently used entry
