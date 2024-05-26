import sys
import os

# Get the path to the src directory
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Add the src directory to the Python path
sys.path.insert(0, src_dir)

import pytest
from database_connection_object_module import DatabaseConnection

class Test_init_dbc():
    # initialize dbc() instance correctly by passing a string
    def test_init_correctly(self):
        my_dbc = DatabaseConnection("https://ows.rasdaman.org/rasdaman/ows")
        assert isinstance(my_dbc.server_url, str)

    # initialize dbc() instance by passing not a string
    def test_init_not_string(self):
        with pytest.raises(TypeError):
            my_dbc = DatabaseConnection(2)

# this tests send_query()
class Test_send_query():
    # send incorrect query
    def test_send_wrong_query(self):
        my_dbc = DatabaseConnection("https://ows.rasdaman.org/rasdaman/ows")
        with pytest.raises(Exception):
            my_dbc.send_query("for $c in")

    # send correct query
    def test_send_correct_query(self):
        my_dbc = DatabaseConnection("https://ows.rasdaman.org/rasdaman/ows")
        response = my_dbc.send_query('for $c in (AvgLandTemp) return 1')
        assert (response.status_code == 200) and (response.content == b'1')

    # pass to the method a variable, which is not a string
    def test_send_not_str(self):
        my_dbc = DatabaseConnection("https://ows.rasdaman.org/rasdaman/ows")
        with pytest.raises(TypeError):
            my_dbc.send_query(1)
