import sys
import os

# Get the path to the src directory
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Add the src directory to the Python path
sys.path.insert(0, src_dir)

import pytest
from datacube_basic_module import Datacube
from database_connection_object_module import DatabaseConnection
from helper_methods import create_good_dco

class Test_aggregation_functions():
    # this tests correct usage of min() -- condition is passed
    def test_proper_input_min(self):
        my_dco = create_good_dco()
        assert isinstance(my_dco.min('$c > 12'), Datacube)
    
    # this tests correct usage of max() -- condition is passed
    def test_proper_input_max(self):
        my_dco = create_good_dco()
        assert isinstance(my_dco.max('$c > 12'), Datacube)
    
    # this tests correct usage of avg() -- condition is passed
    def test_proper_input_avg(self):
        my_dco = create_good_dco()
        assert isinstance(my_dco.avg('$c > 12'), Datacube)
    
    # this tests correct usage of sum() -- condition is passed
    def test_proper_input_sum(self):
        my_dco = create_good_dco()
        assert isinstance(my_dco.sum('$c > 12'), Datacube)
    
    # this tests correct usage of count() -- condition is passed
    def test_proper_input_count(self):
        my_dco = create_good_dco()
        assert isinstance(my_dco.count('$c > 12'), Datacube)
    
    # this tests correct usage of min() -- no arguments
    def test_proper_empty_min(self):
        my_dco = create_good_dco()
        assert isinstance(my_dco.min(), Datacube)
    
    # this tests correct usage of max() -- no arguments
    def test_proper_empty_max(self):
        my_dco = create_good_dco()
        assert isinstance(my_dco.max(), Datacube)

    # this tests correct usage of avg() -- no arguments
    def test_proper_empty_avg(self):
        my_dco = create_good_dco()
        assert isinstance(my_dco.avg(), Datacube)

    # this tests correct usage of sum() -- no arguments
    def test_proper_empty_sum(self):
        my_dco = create_good_dco()
        assert isinstance(my_dco.sum(), Datacube)

    # this tests correct usage of min() -- no arguments
    def test_proper_empty_count(self):
        my_dco = create_good_dco()
        assert isinstance(my_dco.count(), Datacube)

    # this tests method, when the argument passed is not a string - min()
    def test_non_string_arg_min(self):
        my_dco = create_good_dco()
        with pytest.raises(TypeError):
            my_dco.min(2)

    # this tests method, when the argument passed is not a string - max()
    def test_non_string_arg_max(self):
        my_dco = create_good_dco()
        with pytest.raises(TypeError):
            my_dco.max(2)

    # this tests method, when the argument passed is not a string - avg()
    def test_non_string_arg_avg(self):
        my_dco = create_good_dco()
        with pytest.raises(TypeError):
            my_dco.avg(True)

    # this tests method, when the argument passed is not a string - sum()
    def test_non_string_arg_sum(self):
        my_dco = create_good_dco()
        with pytest.raises(TypeError):
            my_dco.sum(False)

    # this tests method, when the argument passed is not a string - count()
    def test_non_string_arg_count(self):
        my_dco = create_good_dco()
        with pytest.raises(TypeError):
            my_dco.count(2)

    # this tests, when the variable passed does not exist - min()
    def test_var_dont_exist_min(self):
        my_dco = create_good_dco()
        with pytest.raises(ValueError):
            my_dco.min('$t < 10001')

    # this tests, when the variable passed does not exist - max()
    def test_var_dont_exist_max(self):
        my_dco = create_good_dco()
        with pytest.raises(ValueError):
            my_dco.max('$t < 10001')

    # this tests, when the variable passed does not exist - avg()
    def test_var_dont_exist_avg(self):
        my_dco = create_good_dco()
        with pytest.raises(ValueError):
            my_dco.avg('$t < 10001')

    # this tests, when the variable passed does not exist - sum()
    def test_var_dont_exist_sum(self):
        my_dco = create_good_dco()
        with pytest.raises(ValueError):
            my_dco.sum('$t < 10001')

    # this tests, when the variable passed does not exist - count()
    def test_var_dont_exist_count(self):
        my_dco = create_good_dco()
        with pytest.raises(ValueError):
            my_dco.count('$t < 10001')

    # this tests that when multiple aggregation functions are used, only the last one is applied
    # first - no condition, second some condition
    def test_last_applied_1(self):
        my_dco = create_good_dco()
        my_dco.min()
        my_dco.max('$c > 12')
        assert (my_dco.aggregation == 'MAX') and (my_dco.aggregation_condition == '$c > 12')

    # this tests that when multiple aggregation functions are used, only the last one is applied
    # first - some condition, second - no condition
    def test_last_applied_2(self):
        my_dco = create_good_dco()
        my_dco.avg('$c > 12')
        my_dco.sum()
        assert (my_dco.aggregation == 'SUM') and (my_dco.aggregation_condition == None)