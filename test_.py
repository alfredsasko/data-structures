'''Modul contains test methods for 7 data structure tasks'''

import pytest
import os

from lru_cache import LRU_Cache
from find_files import FileManager
from compression import HuffmanCompressor


# Tests for task 1: Least Recenty Used Cache
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


# Tests for task 2: Finding Files
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


# Tests for task 3: Huffman Coding
class TestHuffmanCompressor:

    def test_init_method_valid_args(self, valid_hf_set):
        valid_str, hf_tree, encode_map, _ = valid_hf_set
        hc = HuffmanCompressor(valid_str)
        assert ((hc.string == valid_str)
                and (hc._root.to_list() == hf_tree)
                and (hc._encode_map == encode_map))

    def test_init_method_invalid_args(self, invalid_str):
        with pytest.raises(AssertionError):
            hc = HuffmanCompressor(invalid_str)

    def test_encode_method(self, valid_hf_set):
        valid_str, _, _, encoded_str = valid_hf_set
        hc = HuffmanCompressor(valid_str)
        assert hc.encode() == encoded_str

    def test_decode_method_valid_arg(self, valid_hf_set):
        valid_str, _, _, encoded_str = valid_hf_set
        hc = HuffmanCompressor(valid_str)
        assert hc.decode(encoded_str) == valid_str

    def test_decode_method_invalid_arg(self, invalid_hf_set):
        valid_str, invalid_bin_str = invalid_hf_set
        hc = HuffmanCompressor(valid_str)
        with pytest.raises(AssertionError):
            hc.decode(invalid_bin_str)

    def test_decode_method_sum_check_err(
        self, invalid_sum_check_set, sum_check_error):

        string, invalid_encoded_str = invalid_sum_check_set
        hc = HuffmanCompressor(string)

        if sum_check_error == 'ignore':
            assert hc.decode(invalid_encoded_str, sum_check_error) == string

        elif sum_check_error == 'warn':
            with pytest.warns():
                decoded_str = hc.decode(invalid_encoded_str, sum_check_error)
            assert decoded_str == string

        elif sum_check_error == 'raise':
            with pytest.raises(AssertionError):
                decoded_str = hc.decode(invalid_encoded_str, sum_check_error)

        else:
            with pytest.raises(NotImplementedError):
                decoded_str = hc.decode(invalid_encoded_str, sum_check_error)
