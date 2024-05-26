class CoverageConstructor:
    def __init__(self):
        """
        Initializes a new CoverageConstructor instance.
        """
        self.coverage_name = None
        self.axes = []
        self.values_expression = None
    
    def set_coverage_name(self, name):
        """
        Sets the name for the new coverage.

        Parameters:
            name (str): The name to be assigned to the new coverage.

        Returns:
            self: Returns the instance itself for method chaining.
        """
        self.coverage_name = name
        return self
    
    def add_axis(self, name, start, end):
        """
        Adds an axis with the specified name and extent to the coverage.

        Parameters:
            name (str): The name of the axis.
            start (int): The starting value of the axis extent.
            end (int): The ending value of the axis extent.

        Returns:
            self: Returns the instance itself for method chaining.

        Raises:
            ValueError: If the name is not a string, or if start or end are not integers, or if start is greater than or equal to end.
        """
        if not isinstance(name, str):
            raise TypeError("Axis name must be a string.")
        if not isinstance(start, int) or not isinstance(end, int):
            raise TypeError("Axis extents must be integers.")
        if start >= end:
            raise ValueError("Axis start value must be less than its end value.")
        
        self.axes.append((name, start, end))
        return self
    
    def set_values_expression(self, expression=None):
        """
        Sets the expression for computing the coverage's cell values.

        Parameters:
            expression (str): The expression used to compute the cell values.

        Returns:
            self: Returns the instance itself for method chaining.
        """
        if expression is not None and not isinstance(expression, str):
            raise TypeError("Expression must be a string.")

        self.values_expression = expression
        return self

    def reset(self):
        """
        Clears/reset the attributes of the CoverageConstructor instance.

        Returns:
            self: Returns the instance itself for method chaining.
        """
        self.coverage_name = None
        self.axes = []
        self.values_expression = None
        return self
    
    def validate_inputs(self):
        """
        Validates the inputs before generating the coverage query.

        Raises:
            ValueError: If any required attribute is missing or invalid.
        """
        if self.coverage_name is None:
            raise ValueError("Coverage name is not set.")
        if not self.axes:
            raise ValueError("No axes are added.")
        if self.values_expression is None:
            raise ValueError("Values expression is not set.")

    def to_coverage_query(self):
        """
        Generate the coverage query of Coverage Constructor.

        Coverage query example:
        coverage GreyMatrix
        over    $px x imageCrsDomain( $c, Long )
                $py y (imageCrsDomain( $c, Lat )
        values  ( ( $px + $py ) / 2 )

        Returns:
            str: The coverage query.
        """
        self.validate_inputs()
        
        coverage_query = f"coverage {self.coverage_name}\nover "
        for axis in self.axes:
            coverage_query += f"${axis[0]} {axis[1]} : {axis[2]},\n"
        coverage_query += f"values ({self.values_expression})"
        return coverage_query