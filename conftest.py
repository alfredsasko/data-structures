'''Pytest configuration file contains shared fixtures (parameters) for testing.
'''

import pytest
from pytest import fixture
import tempfile
import shutil
from pathlib import Path
import heapq

from lru_cache import LRU_Cache
from find_files import FileManager

# Parameters for testing LRU_Chache class
# ---------------------------------------

# init method
std_capacity = {
    'standard capacity': 5
}

valid_capacity = {
    'positive integer': 5,
}

invalid_capacity = {
    'zero': 0,
    'float': 3.1,
    'negative integer': -3,
    'no number': 'string'
}

# set method
valid_args = {
    'number': 1,
    'string': 'string',
    'none': None,
    'arbitrary object': object()
}


# fixtures
@fixture
def cache():
    return LRU_Cache()

@fixture(params=std_capacity.values(), ids=std_capacity.keys())
def standard_capacity(request):
    return request.param

@fixture(params=valid_capacity.values(), ids=valid_capacity.keys())
def valid_capacity(request):
    return request.param

@fixture(params=invalid_capacity.values(), ids=invalid_capacity.keys())
def invalid_capacity(request):
    return request.param

@fixture(params=valid_args.values(), ids=valid_args.keys())
def key(request):
    return request.param

@fixture(params=valid_args.values(), ids=valid_args.keys())
def value(request):
    return request.param

@fixture
def full_capacity_cache(cache):
    for key in range(cache.capacity):
        if key == 0:
            rlu_key = key
            rlu_value = key
        value = key
        cache.set(key, value)

    new_key = key + 1
    new_value = value + 1
    return new_key, new_value, rlu_key, rlu_value, cache


# Parameters for testing FileManager
# ---------------------------------------

# set here the source and temporary directory for testing
# to ensure that source directory will not be modified by test
src_path = '03_test_directory'
temp_path = 'temp_directory'

valid_path_dict = {
    'string': temp_path,
    'pathlib.Path': Path(temp_path)
}

invalid_path_dict = {
    'not existing path': r'C:\not_existing',
    'no path format': 'no path format',
    'number': 1,
}

in_query_dict = {
    'in_extension_regex': {'query': r'.*\.c$',
                           'regex': True},
    'in_extension': {'query': '.c',
                     'regex': False}
}

out_query_dict = {
    'out_extension_regex': {'query': r'.*\.d$',
                            'regex': True},
    'out_extension': {'query': '.d',
                      'regex': False}
}

invalid_query_dict = {
    'number': {'query': 1}
}

right_files_dict = {
    'in_extension': set([
        temp_path + '/' + 'testdir/subdir1/a.c',
        temp_path + '/' + 'testdir/subdir3/subsubdir1/b.c',
        temp_path + '/' + 'testdir/subdir5/a.c',
        temp_path + '/' + 'testdir/t1.c'
    ])
}

@fixture(scope='class')
def file_manager():
    return FileManager()

@fixture(scope='class')
def temp_directory(src_path=src_path, temp_path=temp_path):

    temp_dir = shutil.copytree(src_path, temp_path, dirs_exist_ok=True)
    yield temp_dir
    shutil.rmtree(temp_dir)

@fixture(params=valid_path_dict.values(), ids=valid_path_dict.keys())
def valid_path(request):
    return request.param

@fixture(params=invalid_path_dict.values(), ids=invalid_path_dict.keys())
def invalid_path(request):
    return request.param

@fixture(params=in_query_dict.values(), ids=in_query_dict.keys())
def in_query(request):
    return request.param

@fixture(params=out_query_dict.values(), ids=out_query_dict.keys())
def out_query(request):
    return request.param

@fixture(params=invalid_query_dict.values(), ids=invalid_query_dict.keys())
def invalid_query(request):
    return request.param

@fixture(params=right_files_dict.values(), ids=right_files_dict.keys())
def right_files(request):
    return request.param


# Parameters for testing HuffmanCompressor
# ---------------------------------------

valid_hf_set_dict = {
    'upper_case_sequence': {
        'string': 'AAAAAAABBBCCCCCCCDDEEEEEE',
        'root': [(25, ''),
                 (11, ''), (14, ''),
                 (5, ''), (6, 'E'), (7, 'A'), (7, 'C'),
                 (2, 'D'), (3, 'B')],
        'encode_map': {'D': '000',
                       'B': '001',
                       'E': '01',
                       'A': '10',
                       'C': '11'},
        'encoded_string':
            '1010101010101000100100111111111111111000000010101010101'
    },
    'one_letter': {
        'string': 'AAAAAAA',
        'encode_map': {'A': '0'},
        'root': [(7, 'A')],
        'encoded_string': '0000000'
    }
}

invalid_str_dict = {
    'empty_string': '',
    'number': 1,
    'list': ['a'],
    'empty_list': [],
    'empty_tuple': tuple()
}

@fixture(params=valid_hf_set_dict.values(), ids=valid_hf_set_dict.keys())
def valid_hf_set(request):
    return (request.param['string'],
            request.param['root'],
            request.param['encode_map'],
            request.param['encoded_string'])

@fixture(params=invalid_str_dict.values(), ids=invalid_str_dict.keys())
def invalid_str(request):
    return request.param
