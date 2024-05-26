import sys
import os

# Get the path to the src directory
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Add the src directory to the Python path
sys.path.insert(0, src_dir)

import pytest
from coverage_constructor import CoverageConstructor


class TestCoverageConstructor:
    # Test set_coverage_name method
    def test_set_coverage_name(self):
        constructor = CoverageConstructor()
        constructor.set_coverage_name("GreyMatrix")
        assert constructor.coverage_name == "GreyMatrix"

    # Test add_axis method
    def test_add_axis(self):
        constructor = CoverageConstructor()
        constructor.add_axis("px", 0, 255)
        constructor.add_axis("py", 0, 255)
        assert constructor.axes == [("px", 0, 255), ("py", 0, 255)]

    # Test set_values_expression method
    def test_set_values_expression(self):
        constructor = CoverageConstructor()
        constructor.set_values_expression("($px + $py) / 2")
        assert constructor.values_expression == "($px + $py) / 2"

    # Test to_coverage_query method
    def test_to_coverage_query(self):
        constructor = CoverageConstructor()
        constructor.set_coverage_name("GreyMatrix")
        constructor.add_axis("px", 0, 255)
        constructor.add_axis("py", 0, 255)
        constructor.set_values_expression("($px + $py) / 2")
        query = constructor.to_coverage_query()
        expected_query = (
            "coverage GreyMatrix\n"
            "over $px 0 : 255,\n"
            "$py 0 : 255,\n"
            "values (($px + $py) / 2)"
        )
        assert query == expected_query
    
    def test_reset(self):
        constructor = CoverageConstructor()
        constructor.set_coverage_name("GreyMatrix")
        constructor.add_axis("px", 0, 255)
        constructor.add_axis("py", 0, 255)
        constructor.set_values_expression("($px + $py) / 2")
        constructor.reset()
        assert constructor.coverage_name is None
        assert constructor.axes == []
        assert constructor.values_expression is None

    # Test to_coverage_query method with missing attributes
    def test_to_coverage_query_missing_attributes(self):
        constructor = CoverageConstructor()
        with pytest.raises(ValueError):
            constructor.to_coverage_query()

    # Test add_axis method with invalid inputs
    def test_add_axis_invalid_inputs(self):
        constructor = CoverageConstructor()
        with pytest.raises(ValueError):
            constructor.add_axis("px", 255, 0)  # Invalid start and end values

    # Test set_values_expression method with invalid input
    def test_set_values_expression_invalid_input(self):
        constructor = CoverageConstructor()
        with pytest.raises(TypeError):
            constructor.set_values_expression(123)  # Invalid expression type

    # Test set_values_expression method with default expression
    def test_set_values_expression_default(self):
        constructor = CoverageConstructor()
        constructor.set_values_expression()  # Test setting default value
        assert constructor.values_expression is None

    # Test coverage query with empty axes
    def test_to_coverage_query_empty_axes(self):
        constructor = CoverageConstructor()
        constructor.set_coverage_name("GreyMatrix")
        constructor.set_values_expression("($px + $py) / 2")
        with pytest.raises(ValueError):
            constructor.to_coverage_query()  # Axes are not added

    # Test coverage query with empty values expression
    def test_to_coverage_query_empty_values_expression(self):
        constructor = CoverageConstructor()
        constructor.set_coverage_name("GreyMatrix")
        constructor.add_axis("px", 0, 255)
        constructor.add_axis("py", 0, 255)
        with pytest.raises(ValueError):
            constructor.to_coverage_query()  # Values expression is not set
