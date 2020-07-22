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
    'arbitrary object': object()
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

@pytest.fixture
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
