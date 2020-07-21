'''Pytest configuration file contains shared fixtures (parameters) for testing.
'''

import pytest
from lru_cache import LRU_Cache

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
    'empty list': [],
    'empty dictionary': {},
    'arbitrary object': object()
}

args_structures = {
    'list': list,
    'set': set,
    'tuple': tuple,
    'dict': dict,
}

args_multiple_structures = {
    'multiple list':['key1', 'value1', 'key2', 'value2'],
    'multiple set': {'key1', 'value1', 'key2', 'value2'},
    'multiple tuple': ('key1', 'value1', 'key2', 'value2'),
    'tuple of tuples': (('key1', 'value1'), ('key2', 'value2')),
    'multiple dict': {'key1': 'value1', 'key2': 'value2'}
}

args_invalid_multiple_structures = {
    'odd items list':['key1', 'value1', 'key2', 'value2'],
    'odd items tuple': ('key1', 'value1', 'key2', 'value2'),
    'tuple of odd tuples': (('key1', 'value1'), ('key2')),
}


# fixtures
@pytest.fixture
def cache():
    return LRU_Cache()

@pytest.fixture(params=std_capacity.values(), ids=std_capacity.keys())
def standard_capacity(request):
    return request.param

@pytest.fixture(params=valid_capacity.values(), ids=valid_capacity.keys())
def valid_capacity(request):
    return request.param

@pytest.fixture(params=invalid_capacity.values(), ids=invalid_capacity.keys())
def invalid_capacity(request):
    return request.param

@pytest.fixture(params=valid_args.values(), ids=valid_args.keys())
def key(request):
    return request.param

@pytest.fixture(params=valid_args.values(), ids=valid_args.keys())
def value(request):
    return request.param

@pytest.fixture(params=args_structures.values(), ids=args_structures.keys())
def key_value_pair(request):
    def _key_value_pair(request, key_, value_):
        if request.param == dict:
            return request.param([(key_, value_)])
        else:
            return request.param((key_, value_))

    return _key_value_pair

@pytest.fixture(params=args_multiple_structures.values(),
                ids = args_multiple_structures.keys())
def multiple_key_value_pair(request):
    return request.param

@pytest.fixture(params=args_invalid_multiple_structures.values(),
                ids = args_invalid_multiple_structures.keys())
def invalid_multiple_key_value_pair(request):
    return request.param
