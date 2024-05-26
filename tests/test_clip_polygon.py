import pytest
import sys
import os

# Get the path to the src directory
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Add the src directory to the Python path
sys.path.insert(0, src_dir)

from wcps_clip_polygon import ClipPolygon

class TestClipPolygon:
    # Test add_point method
    def test_add_point(self):
        polygon = ClipPolygon()
        polygon.add_point(10.0, 20.0)
        assert len(polygon.polygon) == 1
        assert polygon.polygon[0] == "10.0000 20.0000"

    # Test clear_polygon method
    def test_clear_polygon(self):
        polygon = ClipPolygon()
        polygon.add_point(10.0, 20.0)
        polygon.clear_polygon()
        assert len(polygon.polygon) == 0

    # Test is_valid_polygon method
    def test_is_valid_polygon(self):
        polygon = ClipPolygon()
        assert not polygon.is_valid_polygon()  # Empty polygon is not valid

        polygon.add_point(10.0, 20.0)
        assert not polygon.is_valid_polygon()  # Polygon with only one point is not valid

        polygon.add_point(15.0, 25.0)
        assert not polygon.is_valid_polygon()  # Polygon with two points is not valid

        polygon.add_point(10.0, 20.0)  # Add third point to close the loop
        assert polygon.is_valid_polygon()  # Valid polygon with three points

    # Test calculate_polygon_area method
    def test_calculate_polygon_area(self):
        polygon = ClipPolygon()
        polygon.add_point(0, 0)
        polygon.add_point(0, 10)
        polygon.add_point(10, 10)
        polygon.add_point(10, 0)
        assert polygon.calculate_polygon_area() == 100.0

    # Test is_point_inside_polygon method
    def test_is_point_inside_polygon(self):
        polygon = ClipPolygon()
        polygon.add_point(0, 0)
        polygon.add_point(0, 10)
        polygon.add_point(10, 10)
        polygon.add_point(10, 0)
        assert polygon.is_point_inside_polygon(5, 5)
        assert not polygon.is_point_inside_polygon(15, 15)

    # Test to_clip_expression method
    def test_to_clip_expression(self):
        polygon = ClipPolygon()
        polygon.add_point(0, 0)
        polygon.add_point(0, 10)
        polygon.add_point(10, 10)
        polygon.add_point(10, 0)
        assert polygon.to_clip_expression() == "POLYGON((0.0000 0.0000, 0.0000 10.0000, 10.0000 10.0000, 10.0000 0.0000))"

    # Test to_geojson method
    def test_to_geojson(self):
        polygon = ClipPolygon()
        polygon.add_point(0, 0)
        polygon.add_point(0, 10)
        polygon.add_point(10, 10)
        polygon.add_point(10, 0)
        assert polygon.to_geojson() == {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[0.0, 0.0], [10.0, 0.0], [10.0, 10.0], [0.0, 10.0], [0.0, 0.0]]]
            },
            "properties": {}
        }

    def test_rotate_polygon(self):
        polygon = ClipPolygon()
        polygon.add_point(0, 0)
        polygon.add_point(0, 10)
        polygon.add_point(10, 10)
        polygon.add_point(10, 0)
        polygon.rotate_polygon(90, 5, 5)
        assert polygon.polygon == ['10.0000 0.0000', '0.0000 0.0000', '0.0000 10.0000', '10.0000 10.0000']

    # Test scale_polygon method
    def test_scale_polygon(self):
        polygon = ClipPolygon()
        polygon.add_point(0, 0)
        polygon.add_point(0, 10)
        polygon.add_point(10, 10)
        polygon.add_point(10, 0)
        polygon.scale_polygon(2)
        assert polygon.polygon == ['0.0000 0.0000', '0.0000 20.0000', '20.0000 20.0000', '20.0000 0.0000']

