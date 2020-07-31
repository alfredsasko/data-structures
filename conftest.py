'''Pytest configuration file contains shared fixtures (parameters) for testing.
'''

import pytest
from pytest import fixture
import tempfile
import shutil
from pathlib import Path
import heapq
import datetime
import hashlib

from lru_cache import LRU_Cache
from find_files import FileManager
from active_directory import Group

# Task 1: Parameters for testing LRU_Chache class
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


# Task 2: Parameters for testing FileManager
# ------------------------------------------

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


# Task 3: Parameters for testing HuffmanCompressor
# ----------------------------------------------

valid_hf_set_dict = {
    'upper_case_sequence': {
        'string': 'AAAAAAABBBCCCCCCCDDEEEEEE',
        'root': [(25, ''),
                 (11, ''), (14, ''),
                 (5, ''), (6, 'E'), (7, 'A'), (7, 'C'),
                 (2, 'D'), (3, 'B'), None, None, None, None, None, None,
                 None, None, None, None],
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
        'root': [(7, ''),
                 (7, 'A'), None,
                 None, None],
        'encoded_string': '0000000'
    },
    'mixed_sequence': {
        'string': ('Here is the mixed Sequence of 1 number and '
                   'special characters like $ # etc.'),
        'encode_map': {
            ' ': '00', 'H': '010000', 'S': '010001', 'd': '01001', 'a': '0101',
            'k': '011000', 'o': '011001', 'b': '011010', 'f': '011011',
            'p': '011100', 'q': '011101', '#': '011110', '$': '011111',
            'h': '10000', 'l': '10001', 'm': '10010', 'u': '10011',
            'c': '1010', 'x': '101100', '.': '1011010', '1': '1011011',
            'n': '10111', 'e': '110', 's': '11100', 't': '11101',
            'i': '11110', 'r': '11111'
        },
        'root': [
            (75, ''), (30, ''), (45, ''), (14, ' '), (16, ''), (19, ''),
            (26, ''), None, None, (8, ''), (8, ''), (8, ''), (11, ''),
            (12, 'e'), (14, ''), (4, ''), (4, 'a'), (4, ''), (4, ''), (4, ''),
            (4, ''), (5, 'c'), (6, ''), None, None, (6, ''), (8, ''), (2, ''),
            (2, 'd'), None, None, (2, ''), (2, ''), (2, ''), (2, ''), (2, 'h'),
            (2, 'l'), (2, 'm'), (2, 'u'), None, None, (3, ''), (3, 'n'),
            (3, 's'), (3, 't'), (4, 'i'), (4, 'r'), (1, 'H'), (1, 'S'), None,
            None, (1, 'k'), (1, 'o'), (1, 'b'), (1, 'f'), (1, 'p'), (1, 'q'),
            (1, '#'), (1, '$'), None, None, None, None, None, None, None, None,
            (1, 'x'), (2, ''), None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None,
             None, None, None, None, None, None, None, None, None, None, None,
             None, None, (1, '.'), (1, '1'), None, None, None, None
        ],
        'encoded_string': ('01000011011111110001111011100001110110000110001001'
'01111010110011001001000100011100111011001111010111101011000011001011011001011'
'01100101111001110010011010110111110001011011101001001110001110011010101111001'
'01100010010101000001011111101011010111011101111111100001000111110011000110000'
'1111100011110001101110110101011010')
    }
}

invalid_str_dict = {
    'empty_string': '',
    'number': 1,
    'list': ['a'],
    'empty_list': [],
    'empty_tuple': tuple()
}

invalid_hf_set_dict = {
    'non_binary_string': {
        'string': 'AAAAAAA',
        'encoded_string': '0a'
    },
    'non_matched_binary_string': {
        'string': 'AAAAAAA',
        'encoded_string': '1'
    }
}

invalid_sum_check_set_dict = {
    'sum_check_error': {
        'string': 'AAAAAAABBBCCCCCCCDDEEEEEE',
        'encoded_string':
            '10101010101010001001001111111111111110000000101010101010'
    }
}

sum_check_error_dict = {
    'ignore': 'ignore',
    'warning': 'warning',
    'raise': 'raise',
    'not_implemented': 'not_implemented'
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

@fixture(params=invalid_hf_set_dict.values(), ids=invalid_hf_set_dict.keys())
def invalid_hf_set(request):
    return request.param['string'], request.param['encoded_string']

@fixture(params=invalid_sum_check_set_dict.values(),
         ids=invalid_sum_check_set_dict.keys())
def invalid_sum_check_set(request):
    return request.param['string'], request.param['encoded_string']

@fixture(params=sum_check_error_dict.values(), ids=sum_check_error_dict.keys())
def sum_check_error(request):
    return request.param


# Task 4: Parameters for testing Group class
# -------------------------------------------
group_js = {
    'no_nested_group': {
        'name': 'root_group',
        'children': []
    },

    'nested_group': {
        "name": "root_group",
        "children": [
            {
                "name": "child_group",
                "children": []
            }
        ]
    },

    'multiple_nested_group': {
        "name": "root_group",
        "children": [
            {
                "name": "child_group1",
                "children": [
                    {
                        "name": "grand_child1",
                        "children": []
                    },
                    {
                        "name": "grand_child2",
                        "children": []
                    }
                ]
            },
            {
                "name": "child_group2",
                "children": []
            }
        ]
    }
}

user_js = {
    # 'no_user': [],
    'single_user': ['user_1'],
    'multiple_users': ['user_1', 'user_2', 'user_3']
}

in_user_dict = {
    'in_user': 'user_1'
}

out_user_dict = {
    'out_user': 'out_user',
    'no_user': ''
}

@fixture(params=in_user_dict.values(), ids=in_user_dict.keys())
def in_user(request):
    return request.param

@fixture(params=out_user_dict.values(), ids=out_user_dict.keys())
def out_user(request):
    return request.param

@fixture(params=user_js.values(), ids=user_js.keys())
def user_js(request):
    return request.param

@fixture(params=group_js.values(), ids=group_js.keys())
def group_js(request):
    return request.param

@fixture
def group(group_js, user_js):

    def build_group(parent_group, children, users):
        for child in children:
            child_group = Group(child['name'])
            child_group.extend_users(users)
            child_group = build_group(child_group, child['children'], users)
            parent_group.add_group(child_group)
        return parent_group

    root_group = Group(group_js['name'])
    root_group.extend_users(user_js)
    root_children = group_js['children']
    return build_group(root_group, root_children, user_js)


# Taks 5: Parameters for testing Block class
# ------------------------------------------
data_dict = {
    'string': 'string',
    'empty_string': '',
    'number': 1,
    'list': ['a']
}

timestamp_dict = {
    'current_time': datetime.datetime.now()
}

invalid_timestamp_dict = {
    'string': '29-4-2009 10:30:28'
}

prev_hash_dict = {
    'valid_hash': hashlib.sha256(b'string').hexdigest()
}

invalid_prev_hash_dict = {
    'invalid_byte_hash': b'string',
    'invalid_str_hash': 'string'
}

@fixture(params=data_dict.values(), ids=data_dict.keys())
def data(request):
    return request.param

@fixture(params=timestamp_dict.values(), ids=timestamp_dict.keys())
def timestamp(request):
    return request.param

@fixture(params=invalid_timestamp_dict.values(),
         ids=invalid_timestamp_dict.keys())

def invalid_timestamp(request):
    return request.param

@fixture(params=prev_hash_dict.values(), ids=prev_hash_dict.keys())
def prev_hash(request):
    return request.param

@fixture(params=invalid_prev_hash_dict.values(),
         ids=invalid_prev_hash_dict.keys())

def invalid_prev_hash(request):
    return request.param
