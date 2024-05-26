import sys
import os

# Get the path to the src directory
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Add the src directory to the Python path
sys.path.insert(0, src_dir)

import pytest
from datacube_basic_module import Datacube, Coverage
from database_connection_object_module import DatabaseConnection
from expression_builder import Variable, Scalar
from helper_methods import create_good_dco, create_dco

class TestBinaryOperations():
    def test_addition(self):
        # Create a DatacubeObject with a coverage initialized
        my_dco = create_good_dco()

        my_variable = Variable("c")
        variable_with_prefix = my_variable.with_prefix() 
        scalar_value = Scalar(10)
        # Apply addition operation to the coverage in the DatacubeObject
        my_dco.where(variable_with_prefix.add(scalar_value))

        # Assert that the filter condition is correctly applied
        assert my_dco.filter_condition == "$c + 10"
        
    def test_subtraction(self):
        # Create a DatacubeObject with a coverage initialized
        my_dco = create_good_dco()

        my_variable = Variable("c")
        variable_with_prefix = my_variable.with_prefix() 
        scalar_value = Scalar(5)
        # Apply subtraction operation to the coverage in the DatacubeObject
        my_dco.where(variable_with_prefix.subtract(scalar_value))

        # Assert that the filter condition is correctly applied
        assert my_dco.filter_condition == "$c - 5"

    def test_multiplication(self):
        # Create a DatacubeObject with a coverage initialized
        my_dco = create_good_dco()

        my_variable = Variable("c")
        variable_with_prefix = my_variable.with_prefix() 
        scalar_value = Scalar(2)
        # Apply multiplication operation to the coverage in the DatacubeObject
        my_dco.where(variable_with_prefix.multiply(scalar_value))

        # Assert that the filter condition is correctly applied
        assert my_dco.filter_condition == "$c * 2"

    def test_division(self):
        # Create a DatacubeObject with a coverage initialized
        my_dco = create_good_dco()

        my_variable = Variable("c")
        variable_with_prefix = my_variable.with_prefix() 
        scalar_value = Scalar(3)
        # Apply division operation to the coverage in the DatacubeObject
        my_dco.where(variable_with_prefix.divide(scalar_value))

        # Assert that the filter condition is correctly applied
        assert my_dco.filter_condition == "$c / 3"

class TestBinaryOperationsCoverages():
    def test_add_coverages(self):
        # Create mock Coverage objects
        coverage1 = Coverage(["CoverageName1"], "c1")
        coverage2 = Coverage(["CoverageName2"], "c2")
        
        my_dco = create_dco()

        # Call the add_coverages method
        result, final_query = my_dco.add_coverages(coverage1, coverage2)
        
        expected_query = f'For\n$c1 in (CoverageName1),\n$c2 in (CoverageName2)\nreturn\nencode($c1 + $c2, "text/csv")'
        # Assert that the final query matches the expected format
        assert final_query == expected_query

    def test_subtract_coverages(self):
        # Create mock Coverage objects
        coverage1 = Coverage(["CoverageName1"], "c1")
        coverage2 = Coverage(["CoverageName2"], "c2")
        
        my_dco = create_dco()

        # Call the subtract_coverages method
        result, final_query = my_dco.subtract_coverages(coverage1, coverage2)
        expected_query = f'For\n$c1 in (CoverageName1),\n$c2 in (CoverageName2)\nreturn\nencode($c1 - $c2, "text/csv")'

        # Assert that the final query matches the expected format
        assert final_query == expected_query

    def test_multiply_coverages(self):
        # Create mock Coverage objects
        coverage1 = Coverage(["CoverageName1"], "c1")
        coverage2 = Coverage(["CoverageName2"], "c2")

        my_dco = create_dco()
        
        # Call the multiply_coverages method
        result, final_query = my_dco.multiply_coverages(coverage1, coverage2)
        
        expected_query = f'For\n$c1 in (CoverageName1),\n$c2 in (CoverageName2)\nreturn\nencode($c1 * $c2, "text/csv")'

        # Assert that the final query matches the expected format
        assert final_query == expected_query

    def test_divide_coverages(self):
        # Create mock Coverage objects
        coverage1 = Coverage(["CoverageName1"], "c1")
        coverage2 = Coverage(["CoverageName2"], "c2")
        
        my_dco = create_dco()

        # Call the divide_coverages method
        result, final_query = my_dco.divide_coverages(coverage1, coverage2)
        
        expected_query = f'For\n$c1 in (CoverageName1),\n$c2 in (CoverageName2)\nreturn\nencode($c1 / $c2, "text/csv")'

        # Assert that the final query matches the expected format
        assert final_query == expected_query
