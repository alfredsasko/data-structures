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


@pytest.mark.usefixtures('temp_directory')
class TestFileManager:

    def test_find_files_method_valid_path(
        self, file_manager, in_query, valid_path, right_files):

        searched_files = file_manager.find_files(path=valid_path, **in_query)
        assert set(searched_files) == right_files

    def test_find_files_method_file_not_found(
        self, file_manager, out_query, valid_path):

        searched_files = file_manager.find_files(path=valid_path, **out_query)
        assert not searched_files

    def test_find_files_method_invalid_path(
        self, file_manager, in_query, invalid_path):

        with pytest.raises(AssertionError):
            searched_files = file_manager.find_files(
                path=invalid_path, **in_query)

    def test_find_files_method_invalid_query(
        self, file_manager, invalid_query, valid_path):

        with pytest.raises(AssertionError):
            searched_files = file_manager.find_files(
                path=valid_path, **invalid_query)
