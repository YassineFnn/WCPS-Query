import sys
import os
import requests

# Get the path to the src directory
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Add the src directory to the Python path
sys.path.insert(0, src_dir)

import pytest
from datacube_basic_module import Datacube
from database_connection_object_module import DatabaseConnection
from expression_builder import Variable, Scalar
from helper_methods import create_good_dco, create_dco

class Test_init_dco():
    # init by not passing a dbc() instance
    def test_not_correct_dbc(self):
        with pytest.raises(TypeError):
            my_dco = DatabaseConnection(2)

    # init correct dbc() instance
    def test_pass_dbc(self):
        my_dbc = DatabaseConnection("https://ows.rasdaman.org/rasdaman/ows")
        my_dco = Datacube(my_dbc)
        assert isinstance(my_dco.dbc, DatabaseConnection)

# this tests initialization of the variable in the dco()
class Test_init_var():
    # init_var gets a string in a correct format
    def test_good_format(self):
        my_dco = create_dco()
        assert isinstance(my_dco.coverage_instance("AvgLandTemp", "c"), Datacube)
    
    # init_var gets not a string
    def test_type_error(self):
        my_dco = create_dco()
        with pytest.raises(TypeError):
            my_dco.coverage_instance()
    
    # init_var gets a string in not correct format
    def test_format_error(self):
        my_dco = create_dco()
        with pytest.raises(TypeError):
            my_dco.coverage_instance(12, 32)

# this tests subset()
class Test_subset():
    # pass correct values as a subset
    def test_correct_subset(self):
        my_dco = create_good_dco()
        assert isinstance(my_dco.subset(var_name = '$c', subset = 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")'), Datacube)
    
    # don't pass one of the arguments
    def test_dont_pass_one_arg(self):
        my_dco = create_good_dco()
        with pytest.raises(TypeError):
            my_dco.subset(var_name = '$c')

    # pass as an argument not a string to the var_name argument
    def test_pass_not_str_varname(self):
        my_dco = create_good_dco()
        with pytest.raises(TypeError):
            my_dco.subset(var_name = 2, subset = 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")')
    
    # pass as an argument not a string to the subset argument
    def test_pass_not_str_subset(self):
        my_dco = create_good_dco()
        with pytest.raises(TypeError):
            my_dco.subset(var_name = '$c', subset = 1000)

    # pass as an argument not existing variable
    def test_pass_non_existing_var(self):
        my_dco = create_good_dco()
        with pytest.raises(ValueError):
            my_dco.subset(var_name = '$t', subset = 'Lat(53.08), Long(8.80), ansi("2014-01":"2014-12")')

# this tests set_format() method
class Test_set_format():
    # pass an existing format(PNG)
    def test_correct_format_png(self):
        my_dco = create_good_dco()
        assert isinstance(my_dco.set_format('PNG'), Datacube)

    # pass an existing format(CSV)
    def test_correct_format_csv(self):
        my_dco = create_good_dco()
        assert isinstance(my_dco.set_format('CSV'), Datacube)
    
    # pass an existing format(JPEG)
    def test_correct_format_jpeg(self):
        my_dco = create_good_dco()
        assert isinstance(my_dco.set_format('JPEG'), Datacube)

    # pass nothing
    def test_pass_nothing(self):
        my_dco = create_good_dco()
        with pytest.raises(TypeError):
            my_dco.set_format()

    # pass non-string argument
    def test_pass_non_string(self):
        my_dco = create_good_dco()
        with pytest.raises(TypeError):
            my_dco.set_format(2)

    # pass non-existing format
    def test_pass_non_existing_format(self):
        my_dco = create_good_dco()
        with pytest.raises(ValueError):
            my_dco.set_format('TIFF')

# this tests where() method
class Test_where:
    # pass an argument with existing var. name and in a string format
    def test_pass_correct(self):
        my_dco = create_good_dco()
        assert isinstance(my_dco.where(Variable("c").greater_than(Scalar(2))), Datacube)

    # pass nothing
    def test_pass_nothing(self):
        my_dco = create_good_dco()
        with pytest.raises(TypeError):
            my_dco.where()

    # pass a filter condition with non-existing variable
    def test_pass_non_existing_var(self):
        my_dco = create_good_dco()
        with pytest.raises(ValueError):
            my_dco.where(Variable("t").greater_than(Scalar(10)))

    # pass non-string argument
    def test_pass_non_string_arg(self):
        my_dco = create_good_dco()
        with pytest.raises(TypeError):
            my_dco.where(Scalar(2))
            
# this tests transform_data() method
class Test_transform_data():
    # this tests when the correct transformation operation is passed
    def test_correct_trans_operation(self):
        my_dco = create_good_dco()
        assert isinstance(my_dco.transform_data('abs($c - 1000)'), Datacube)

    # this tests when nothing is passed
    def test_nothing_passed(self):
        my_dco = create_good_dco()
        with pytest.raises(TypeError):
            my_dco.transform_data()

    # this tests when the transformation operation is applied to non existing variable
    def test_non_existing_var(self):
        my_dco = create_good_dco()
        with pytest.raises(ValueError):
            my_dco.transform_data('200 - 100')

    # this tests when the operation passed isn't a string
    def test_non_string_arg(self):
        my_dco = create_good_dco()
        with pytest.raises(TypeError):
            my_dco.transform_data(200)

# this tests encode() function
class Test_encode():
    # nothing is passed
    def test_no_arg(self):
        my_dco = create_good_dco()
        with pytest.raises(TypeError):
            my_dco.encode()

    # non-string operation is passed
    def test_non_string_arg(self):
        my_dco = create_good_dco()
        my_dco.encode(200)
        assert isinstance(my_dco.encode_as, str)

    # this tests when a string passed doesn't have existing variables
    def test_non_exist_vars(self):
        my_dco = create_good_dco()
        with pytest.raises(ValueError):
            my_dco.encode('$t > 12')
    
    # this tests when the correct operation is passed
    def test_correct_format(self):
        my_dco = create_good_dco()
        assert isinstance(my_dco.encode('$c > 12'), Datacube)

# this tests to_wcps_query()
class Test_construct_query():
    # because to_wcps_query() is supposed to be used only by execute() method, we don't expect that non-string argument
    # is passed, because all our methods check that

    # this tests when the correct input is given to the method
    def test_correct_input(self):
        my_dco = create_good_dco()
        my_dco.subset(var_name = '$c', subset = 'ansi("2014-07")')
        my_dco.set_format('PNG')
        assert (my_dco.construct_query() == 'for $c in (AvgLandTemp)\nreturn \nencode($c[ansi("2014-07")] , "image/png")')

    # this tests when the format is not given
    def test_no_format(self):
        my_dco = create_good_dco()
        my_dco.subset(var_name = '$c', subset = 'ansi("2014-07")')
        my_dco.encode(200 + 100)
        assert my_dco.construct_query() == 'for $c in (AvgLandTemp)\nreturn \nencode(300, "text/csv")'

    # this tests when transformation is given first and then encoding
    def test_trans_then_encode(self):
        my_dco = create_good_dco()
        my_dco.subset(var_name = '$c', subset = 'ansi("2014-07")')
        my_dco.transform_data('$c + 200')
        my_dco.encode(200 + 100)
        assert my_dco.construct_query() == 'for $c in (AvgLandTemp)\nreturn \nencode(300, "text/csv")'
    
class TestQueryExecution:
    # Test case to check the query execution result against expected result
    def test_query_execution(self):
        my_dco = create_good_dco()
        my_dco.subset(var_name='$c', subset='ansi("2014-07")')
        my_dco.set_format('PNG')
        result = my_dco.execute()
        
        # Fetch the expected PNG data
        expected_png_url = "https://ows.rasdaman.org/rasdaman/ows?SERVICE=WCS&VERSION=2.0.1&REQUEST=ProcessCoverages&QUERY=for%20%24c%20in%20(AvgLandTemp)%20return%20%0Aencode(%24c%5Bansi(%222014-07%22)%5D%20%2C%20%22PNG%22)"
        expected_response = requests.get(expected_png_url)
        
        # Assert that the response status code is 200 (OK)
        assert expected_response.status_code == 200
        
        # Compare the content of the obtained PNG data and the expected PNG data
        assert result == expected_response.content