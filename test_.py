'''Modul contains test methods for LRU_Cache class'''

import pytest
from lru_cache import LRU_Cache
from find_files import FileManager
import os


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


class TestFileManager:

    def test_init_method_no_args(self):
        file_manager = FileManager()
        assert file_manager.root == os.getcwd()

    def test_init_method_valid_args(self, valid_path):
        file_manager = FileManager(valid_path)
        assert file_manager.root == valid_path

    def test_init_method_invalid_args(self, invalid_path):
        with pytest.raises(AssertionError):
            file_manger = FileManager(invalid_path)
