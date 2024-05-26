# Classes in 'wdc'

## Class: DatabaseConnection
This class provides a method for sending WCPS queries to the specified server endpoints and handling the responses. It also includes error handling protocol and provides useful feedback in case something goes wrong with the network communication or server response.

### Attributes
| Name | Data type |
| --- | --- |
| Server_url | string |

### Methods
| Name | Return |
| --- | --- |
| send_query | Object from the server |

***send_query(wcps_query)***: First, it initializes a new ‘DatabaseConnection’ instance with ‘url’, which will serve as an endpoint URL of the WCPS server.

## Class: Datacube

This class represents a datacube and provides methods for manipulation and querying.

### Attributes
| Name | Data type |
| --- | --- |
| dbc | DatabaseConnection |
| variables | list |
| variable_names | list |
| subsets | list |
| aggregation | str |
| aggregation_condition | str |
| format | str |
| encode_as | str |
| filter | str |
| transformation | str |
| switch_str | str |

### Methods
| Name | Parameter | Return |
| --- | --- | --- |
| \_\_init\_\_ | dbc_used | - |
| reset | - | Datacube |
| get_all_var_names | string | list | 
| do_vars_exist | string | bool |
| coverage_instance | coverage_name, var_name | Datacube |
| subset | subset, var_name | Datacube |
| where | filter_condition | Datacube |
| switch | condition, cases, default_case | str |
| min | condition | Datacube |
| max | condition | Datacube |
| avg | condition | Datacube |
| sum | condition | Datacube |
| count | condition | Datacube |
| replace_variables_with_subsets | str_to_transform | str |
| transform_data | operation | Datacube |
| set_aggregation | wanted | str |
| set_format | output_format | Datacube |
| return_format | - | str |
| encode | operation | self |
| construct_query | - | str |
| execute | - | str or list |
| add_coverages | \*coverages | Coverage, str |
| subtract_coverages | \*coverages | Coverage, str |
| multiply_coverages | \*coverages | Coverage, str |
| divide_coverages | \*coverages | Coverage, str |

***\_\_init\_\_(dbc_used)***: Initializes a Datacube instance with a DatabaseConnection object.

***reset()***: Resets the attributes of the Datacube instance to their default values, except for the database connection (dbc), which remains unchanged.

***get_all_var_names(string)***: Extracts all variable names from a string where variables are prefixed by '$'.

***do_vars_exist(string)***: Checks whether all variable names extracted from the input string exist in the predefined list of variable names of the current instance.

***coverage_instance(coverage_name, var_name)***: Adds a coverage variable to the Datacube instance.

***subset(subset, var_name)***: Adds a subset specification to the Datacube instance.

***where(filter_condition)***: Sets a filter condition for the datacube query.

***switch(condition, cases, default_case)***: Constructs a switch statement in a WCPS query with multiple cases.

***min(condition)***: Configures the datacube to compute the minimum value of the specified data subset when executed.

***max(condition)***: Configures the datacube to compute the maximum value of the specified data subset when executed.

***avg(condition)***: Configures the datacube to compute the average value of the specified data subset when executed.

***sum(condition)***: Configures the datacube to compute the sum of values across the specified data subset when executed.

***count(condition)***: Configures the datacube to count the number of data points that meet the specified condition when executed.

***replace_variables_with_subsets(str_to_transform)***: Replaces variables in a given string with their corresponding subsets if defined.

***transform_data(operation)***: Sets a transformation operation to be applied to the datacube when the query is executed.

***set_aggregation(wanted)***: Sets the aggregation operation for the datacube query.

***set_format(output_format)***: Sets the output format for the datacube query.

***return_format()***: Determines the format for the output based on the configured settings of the datacube.

***encode(operation)***: Specifies the encoding operation to be applied to the output of the query.

***construct_query()***: Constructs a WCPS query based on the configured settings of the datacube.

***execute()***: Executes the constructed WCPS query and processes the response based on the specified format.

***add_coverages(\*coverages)***: Adds multiple coverages together and returns the result as a new coverage.

***subtract_coverages(\*coverages)***: Subtracts multiple coverages and returns the result as a new coverage.

***multiply_coverages(\*coverages)***: Multiplies multiple coverages together and returns the result as a new coverage.

***divide_coverages(\*coverages)***: Divides multiple coverages and returns the result as a new coverage.



***byte_to_list()***: This utility function decodes the byte string to a regular string using ‘UTF-8’ encoding.

## Class: Variable
This class represents a variable used in expressions and conditions. It provides methods for comparing variables and building logical expressions.

### Attributes
| Name | Data type |
| --- | --- |
| name | string |


### Methods
| Name | Parameter | Return |
| --- | --- | --- |
| init | string | - |
| greater_than | Variable | string | 
| less_than | Variable | string | 
| and_ | - | string | 

***init(name)***:
This method creates a new Variable object and assigns the given name to its internal name attribute.

***greater_than(other)***:
This method creates a string representing the variable being greater than another variable or value. It uses string formatting to insert the variable's name and the other value.

***less_than(other)***:
Similar to greater_than, this method creates a string representing the variable being less than another variable or value.

***and_()***:
This method simply returns the string " and " which can be used to build logical expressions involving multiple variables.

## Class: Scalar

This class represents a scalar value and provides methods to perform basic arithmetic operations.

### Attributes
| Name | Data type |
| --- | --- |
| value | varies |

### Methods
| Name | Parameter | Return |
| --- | --- | --- |
| `__init__(value)` | value | - |
| `__str__` | - | string |
| `add(other)` | Scalar | string | 
| `subtract(other)` | Scalar | string | 
| `multiply(other)` | Scalar | string | 
| `divide(other)` | Scalar | string | 

***`__init__(value)`***: Initializes a Scalar object with the given value.

***`__str__`***: Returns a string representation of the scalar value.

***`add(other)`***: Performs addition between this scalar and another scalar.

***`subtract(other)`***: Performs subtraction between this scalar and another scalar.

***`multiply(other)`***: Performs multiplication between this scalar and another scalar.

***`divide(other)`***: Performs division between this scalar and another scalar.

## Class: Coverage

This class represents a coverage and provides methods for arithmetic operations between coverages.

### Attributes
| Name | Data type |
| --- | --- |
| coverage_names | varies |
| variable_name | varies |

### Methods
| Name | Parameter | Return |
| --- | --- | --- |
| \_\_init\_\_ | coverage_names, varirable_name | - |
| \_\_add\_\_ | Coverage | BinaryOperation | 
| \_\_sub\_\_ | Coverage | BinaryOperation | 
| \_\_mul\_\_ | Coverage | BinaryOperation | 
| \_\_truediv\_\_ | Coverage | BinaryOperation | 

***\_\_init\_\_(coverage_names, var_name)***: Initializes a Coverage object with the given coverage names and variable name.

***\_\_add\_\_(other)***: Creates a BinaryOperation instance for addition if the operand is also a Coverage.

***\_\_sub\_\_(other)***: Creates a BinaryOperation instance for subtraction if the operand is also a Coverage.

***\_\_mul\_\_(other)***: Creates a BinaryOperation instance for multiplication if the operand is also a Coverage.

***\_\_truediv\_\_(other)***: Creates a BinaryOperation instance for division if the operand is also a Coverage.

## Class: BinaryOperation

This class represents a binary operation between two coverages.

### Attributes
| Name | Data type |
| --- | --- |
| lhs | Coverage |
| rhs | Coverage |
| operation | string |

### Methods
| Name | Parameter | Return |
| --- | --- | --- |
| \_\_init\_\_ | lhs, rhs, operation | - |

***\_\_init\_\_(lhs, rhs, operation)***: Initializes a BinaryOperation object with the left-hand side coverage, right-hand side coverage, and operation type.

## Class: ClipPolygon

This class represents a polygon for clipping in a WCPS query and provides methods for manipulating and generating clip expressions.

### Attributes
| Name | Data type | Description |
| --- | --- | --- |
| polygon | list of str | List of points in the polygon. Each point is represented as a string in the format "lat long". |

### Methods
| Name | Parameters | Return | Description |
| --- | --- | --- | --- |
| \_\_init\_\_ | - | - | Initializes a new ClipPolygon instance. |
| add_point | lat (float), long (float) | ClipPolygon | Adds a point to the POLYGON in the WCPS query. |
| clear_polygon | - | - | Clears all points from the polygon. |
| is_valid_polygon | - | bool | Checks if the polygon is valid. |
| calculate_polygon_area | - | float | Calculates the area of the polygon using the shoelace formula. |
| is_point_inside_polygon | lat (float), lon (float) | bool | Checks if a given point is inside the polygon. |
| to_clip_expression | - | str | Generates the clip expression for the POLYGON. |
| to_geojson | - | dict | Converts the polygon to GeoJSON format. |
| rotate_polygon | angle (float), center_lat (float), center_lon (float) | - | Rotates the polygon by a specified angle around a given center point. |
| scale_polygon | factor (float) | - | Scales the polygon by a given factor around a specified center point. |

### Method Details
***\_\_init\_\_()***: Initializes a new ClipPolygon instance.

***add_point(lat: float, long: float)***: Adds a point to the POLYGON in the WCPS query.

***clear_polygon()***: Clears all points from the polygon.

***is_valid_polygon()***: Checks if the polygon is valid.

***calculate_polygon_area()***: Calculates the area of the polygon using the shoelace formula.

***is_point_inside_polygon(lat: float, lon: float)***: Checks if a given point is inside the polygon.

***to_clip_expression()***: Generates the clip expression for the POLYGON.

***to_geojson()***: Converts the polygon to GeoJSON format.

***rotate_polygon(angle: float, center_lat: float, center_lon: float)***: Rotates the polygon by a specified angle around a given center point.

***scale_polygon(factor: float)***: Scales the polygon by a given factor around a specified center point.


## Class: CoverageConstructor

This class represents a coverage constructor and provides methods for configuring and generating coverage queries.

### Attributes
| Name | Data type | Description |
| --- | --- | --- |
| coverage_name | str | The name of the coverage being constructed. |
| axes | list of tuples | List of axis names and extents. |
| values_expression | str | The expression used to compute the cell values of the coverage. |

### Methods
| Name | Parameters | Return | Description |
| --- | --- | --- | --- |
| \_\_init\_\_ | - | - | Initializes a new CoverageConstructor instance. |
| set_coverage_name | name (str) | self | Sets the name for the new coverage. |
| add_axis | name (str), start (int), end (int) | self | Adds an axis with the specified name and extent to the coverage. |
| set_values_expression | expression (str) | self | Sets the expression for computing the coverage's cell values. |
| reset | - | self | Clears/reset the attributes of the CoverageConstructor instance. |
| validate_inputs | - | - | Validates the inputs before generating the coverage query. |
| to_coverage_query | - | str | Generates the coverage query of Coverage Constructor. |

### Method Details
***\_\_init\_\_()***: Initializes a new CoverageConstructor instance.

***set_coverage_name(name: str)***: Sets the name for the new coverage.

***add_axis(name: str, start: int, end: int)***: Adds an axis with the specified name and extent to the coverage.

***set_values_expression(expression: str)***: Sets the expression for computing the coverage's cell values.

***reset()***: Clears/reset the attributes of the CoverageConstructor instance.

***validate_inputs()***: Validates the inputs before generating the coverage query.

***to_coverage_query()***: Generates the coverage query of Coverage Constructor.


### Example Coverage Query:
```
for $c in ( AvgLandTemp ) 
return encode(
                coverage myCoverage
                over $p x(0:200),
                     $q y(0:200)
                values $p + $q
    , "image/png")
```
```
for $c in ( AvgLandTemp ) 
return encode(
                coverage myCoverage
                over $t temp(0:20)
                values 
                    count(c[ansi("2005-07")]>=0 )and(c[ansi("2005-07")]<1)
    , "csv")
```