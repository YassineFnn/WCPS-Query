from datacube_basic_module import Datacube
from database_connection_object_module import DatabaseConnection

# we will get coverages from the https://ows.rasdaman.org/rasdaman/ows
def create_dco():
    my_dbc = DatabaseConnection("https://ows.rasdaman.org/rasdaman/ows")
    my_dco = Datacube(my_dbc)
    return my_dco

def create_good_dco():
    my_dbc = DatabaseConnection("https://ows.rasdaman.org/rasdaman/ows")
    my_dco = Datacube(my_dbc)
    return my_dco.coverage_instance("AvgLandTemp", "c")

def create_good_dco_binary():
    my_dbc = DatabaseConnection("https://ows.rasdaman.org/rasdaman/ows")
    my_dco = Datacube(my_dbc)
    my_dco.coverage_instance("AvgLandTemp", "c1")
    my_dco.coverage_instance("AvgLandTemp", "c2")
    return my_dco