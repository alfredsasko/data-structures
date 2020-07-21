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
        pytest.skip()
        cache.set(key, value)
        assert (cache.memory[key] == value)

    def test_set_method_args_structure(self, cache, key_value_pair):
        pytest.skip()
        key, value = 'key', 'value'
        key_value = key_value_pair(key, value)
        if isinstance(key_value, set):
            with pytest.raises(AssertionError):
                cache.set(key_value)
        else:
            assert (cache.memory[key] == value)

    def test_set_method_args_multiple_structure(
        self, cache, multiple_key_value_pair):

        pytest.skip()
        key_value = key_value_pair(multiple_value_pair)
        if isinstance(multiple_value_pair, set):
            with pytest.raises(AssertionError):
                cache.set(multiple_value_pair)
        else:
            for key, value in multiple_key_value_pair:
                assert (cache.memory[key] == value)

    def test_set_method_args_invalid_multiple_structure(
        self, cache, invalid_multiple_key_value_pair):

        pytest.skip()
        with pytest.raises(AssertionError):
            cache.set(invalid_multiple_key_value_pair)

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
