from database_connection_object_module import DatabaseConnection
from byte_to_list_module import byte_to_list
import re

class Datacube:
    def __init__(self, dbc_used):
        """
        Initializes a Datacube instance with a DatabaseConnection object.

        Parameters:
            dbc_used (DatabaseConnection): The DatabaseConnection object used for querying.

        Raises:
            TypeError: If dbc_used is not an instance of DatabaseConnection.
        """
        if not isinstance(dbc_used, DatabaseConnection):
            raise TypeError("dbc instance not passed")
        
        self.dbc = dbc_used
        self.variables = []
        self.variable_names = []
        self.subsets = []
        self.aggregation = None
        self.aggregation_condition = None
        self.format = None
        self.encode_as = None
        self.filter = None
        self.transformation = None
        self.switch_str = None
        
    def reset(self):
        """
        Resets the attributes of the Datacube instance to their default values,
            except for the database connection (dbc), which remains unchanged.

        Returns:
            Datacube: Returns the instance itself with reset values.
        """
        self.variables = []
        self.variable_names = []
        self.subsets = []
        self.aggregation = None
        self.aggregation_condition = None
        self.format = None
        self.encode_as = None
        self.filter = None
        self.transformation = None
        self.switch_str = None
        return self
    
    def get_all_var_names(self, string):
        """
        Extracts all variable names from a string where variables are prefixed by '$' and can be
            followed by various delimiters such as spaces, commas, parentheses, etc.

        Parameters:
            string (str): A string potentially containing multiple variables each prefixed by '$'.

        Returns:
            list: A list of extracted variable names. Returns an empty list if no variables are found.

        Example:
            >>> var_names = get_all_var_names("$a>15 and $b")
            >>> print(var_names)
            ['$a', '$b']
        """
        pattern = r'\$[a-zA-Z_][a-zA-Z0-9_]*'  # Regular expression pattern to match variable names
        var_names = re.findall(pattern, string)
        
        if len(var_names) == 0:
            return None
        
        return var_names
    
    def do_vars_exist(self, string):
        """
        Checks whether all variable names extracted from the input string exist in the predefined list of
        variable names of the current instance. This method is useful for validating that variables
        referenced in a string (e.g., a query or command) are all recognized by the system
        before proceeding with further operations.

        Parameters:
            string (str): The string from which variable names are extracted and checked.
                Variables in the string should be prefixed by '$'.

        Returns:
            bool: True if all extracted variables exist in the instance's variable list.

        Raises:
            ValueError: If no variables are specified in the string, or
            if one or more variables do not exist in the instance's list of variables.

        Example:
            >>> datacube.do_vars_exist("$temp and $pressure")
            True
            >>> datacube.do_vars_exist("$humidity")
            Traceback (most recent call last):
            ...
            ValueError: Variables in a string don't exist
        """
        # Normalize the string by replacing multiple whitespace characters with a single space
        string = re.sub(r'\s+', ' ', string)
        
        var_names = self.get_all_var_names(string)

        if var_names:
            var_names = set(var_names)
            # Convert the list of variable names to a set for efficient comparison
            if var_names.issubset(set(self.variable_names)):
                return True
            else:
                raise ValueError("Variables in a string don't exist")
        else:
            raise ValueError("Variables weren't specified")

    def coverage_instance(self, coverage_name, var_name):
        """
        Adds a coverage variable to the Datacube instance.

        Parameters:
            coverage_name (str): The name of the coverage.
            var_name (str): The name of the variable.

        Returns:
            Datacube: Returns the instance itself for method chaining.
        """
        # Check if coverage_name and var_name are strings
        if not isinstance(coverage_name, str) or not isinstance(var_name, str):
            raise TypeError("Both arguments must be strings.")
        
        # Create the variable string in the specified format
        variable_string = f"${var_name} in ({coverage_name})"
        variable_name = f"${var_name}"
        
        # Add the variable string to the list of variables
        self.variables.append(variable_string)
        
        # Add the coverage_name as a variable name
        self.variable_names.append(variable_name)
        
        # Add None to subsets (no subset defined yet)
        self.subsets.append(None)
        return self
        
    def subset(self, subset, var_name=None):
        """
        Adds a subset specification to the Datacube instance.

        Parameters:
            subset (str): The subset specification.
            var_name (str, optional): The name of the variable. If None, a generic label is generated.

        Returns:
            Datacube: Returns the instance itself for method chaining.

        Raises:
            TypeError: If subset is not a string or var_name is provided but not a string.
            ValueError: If var_name is provided but not found in the list of variable names.
        """
        # Consider all combinations of lat, long, ansi
        if not isinstance(subset, str):
            raise TypeError("Subset must be a string.")
        
        if var_name is not None:
            if not isinstance(var_name, str):
                raise TypeError("Variable name must be a string.")
            if var_name not in self.variable_names:
                raise ValueError("Variable name does not exist.")
            # Index of the variable name in the variable_names list
            idx = self.variable_names.index(var_name)
        else:
            # If variable name is not provided, use a generic label
            idx = len(self.variable_names)  # Next available index
            var_name = f"result{idx + 1}"  # Generate a generic label
            
        # Update the subset specification at the corresponding index in the subsets list
        if idx < len(self.subsets):
            self.subsets[idx] = subset
        else:
            # If idx is out of range, extend the subsets list
            self.subsets.extend([None] * (idx - len(self.subsets)))
            self.subsets.append(subset)
            
        # If var_name is not in variable_names, add it
        if var_name not in self.variable_names:
            self.variable_names.append(var_name)
        
        return self
    
    def where(self, filter_condition):
        """
        Sets a filter condition for the datacube query.

        Parameters:
            filter_condition (str): A string representing the condition to be applied to filter the data.

        Returns:
            Datacube: Returns the instance itself for method chaining.

        Raises:
            TypeError: If filter_condition is not a string.
        """
        if not isinstance(filter_condition, str):
            raise TypeError("Value entered must be a string.")

        # Check if any variables in the condition string are not present in the datacube
        if not isinstance(filter_condition, str):
            raise TypeError("Value entered must be a string.")

        self.do_vars_exist(filter_condition)

        self.filter_condition = filter_condition
        return self
    
    def switch(self, condition, cases, default_case):
        """
        Constructs a switch statement in a WCPS query with multiple cases.

        Parameters:
            condition (str): The condition to evaluate.
            cases (list): A list of tuples where each tuple contains the condition and the expression for that case.
            default_case (str): The expression to return if none of the conditions are met.

        Returns:
            str: The constructed switch statement in a WCPS query.
        """
        switch_statement = f"switch case {condition}"
        for case_condition, case_expression in cases:
            switch_statement += f" {case_condition} return {case_expression}"
        switch_statement += f" default return {default_case} end"
        self.switch_str = switch_statement
        return self

    # Aggregation methods
    # Each method sets an aggregation operation and an optional condition
    def min(self, condition=None):
        """
        Configures the datacube to compute the minimum value of the specified data subset when executed.

        Parameters:
            condition (str, optional): A condition that defines the subset of data for which the minimum is calculated.

        Returns:
            Datacube: Returns the instance itself for method chaining.

        Raises:
            TypeError: If condition is provided and not a string.
        """
        if condition != None:
            if not isinstance(condition, str):
                raise TypeError("Value entered must be a string.")
            self.do_vars_exist(condition)
        self.aggregation_condition = condition
        self.aggregation = 'MIN'
        return self
        
    def max(self, condition=None):
        """
        Configures the datacube to compute the maximum value of the specified data subset when executed.

        Parameters:
            condition (str, optional): A condition that defines the subset of data for which the maximum is calculated.

        Returns:
            Datacube: Returns the instance itself for method chaining.

        Raises:
            TypeError: If condition is provided and not a string.
        """
        if condition != None:
            if not isinstance(condition, str):
                raise TypeError("Value entered must be a string.")
            self.do_vars_exist(condition)
        self.aggregation_condition = condition
        self.aggregation = 'MAX'
        return self
    
    def avg(self, condition=None):
        """
        Configures the datacube to compute the average value of the specified data subset when executed.

        Parameters:
            condition (str, optional): A condition that defines the subset of data for which the average is calculated.

        Returns:
            Datacube: Returns the instance itself for method chaining.

        Raises:
            TypeError: If condition is provided and not a string.
        """
        if condition != None:
            if not isinstance(condition, str):
                raise TypeError("Value entered must be a string.")
            self.do_vars_exist(condition)
        self.aggregation_condition = condition
        self.aggregation = 'AVG'
        return self
    
    def sum(self, condition=None):
        """
        Configures the datacube to compute the sum of values across the specified data subset when executed.

        Parameters:
            condition (str, optional): A condition that defines the subset of data for which the sum is calculated.

        Returns:
            Datacube: Returns the instance itself for method chaining.

        Raises:
            TypeError: If condition is provided and not a string.
        """
        if condition != None:
            if not isinstance(condition, str):
                raise TypeError("Value entered must be a string.")
            self.do_vars_exist(condition)
        self.aggregation_condition = condition
        self.aggregation = 'SUM'
        return self
        
    def count(self, condition=None):
        """
        Configures the datacube to count the number of data points that meet the specified condition when executed.

        Parameters:
            condition (str, optional): A condition that specifies the criteria that data points must meet to be counted.

        Returns:
            Datacube: Returns the instance itself for method chaining.

        Raises:
            TypeError: If condition is provided and not a string.
        """
        if condition != None:
            if not isinstance(condition, str):
                raise TypeError("Value entered must be a string.")
            self.do_vars_exist(condition)
        self.aggregation = 'COUNT'
        self.aggregation_condition = condition
        return self
    
    def replace_variables_with_subsets(self, str_to_transform=None):
        """
        Replaces variables in a given string with their corresponding subsets if defined.
            If no string is provided, it constructs a string representation of
            all variables and their subsets.

        Parameters:
            str_to_transform (str, optional): A string containing variable names that need to be replaced with their subsets.

        Returns:
            str: A new string with variables replaced by their subsets,
                or a concatenated string of all variables and subsets.

        Example:
            >>> datacube.replace_variables_with_subsets("abs($c - 200)")
            >>> "abs($c[corresponding_subset] - 200)"
        """
        # This distinction is critical as it determines the course of action
        # code will either modify an existing string or create a new list of all variables and their subsets.
        if str_to_transform != None:
            expression = str_to_transform
            # Iterate over tuples of variables and corresponding subsets
            for var, subset in zip(self.variable_names, self.subsets):
                if subset != None:
                    # Replace the variable in the expression with its subset
                    expression = expression.replace(var, f'{var}[{subset}]')
            return expression
        else:
            expression = ''
            for var, subset in zip(self.variable_names, self.subsets):
                if subset != None:
                    # If a subset exists, append the variable and its subset in bracketed form
                    expression += f'''{var}[{subset}] '''
                else:
                    # If no subset exists, simply append the variable
                    expression += f'''{var}'''
            return expression
        
    def transform_data(self, operation):
        """
        Sets a transformation operation to be applied to the datacube when the query is executed.

        Parameters:
            operation (str): A string representing the transformation operation to be applied.

        Returns:
            Datacube: Returns the instance itself for method chaining.

        Raises:
            TypeError: If operation is not a string.
        """
        if not isinstance(operation, str):
            raise TypeError("Value entered must be a string.")
        self.do_vars_exist(operation)
        self.transformation = operation
        return self
        
    def set_aggregation(self, wanted:str):
        """
        Sets the aggregation operation for the datacube query.

        Parameters:
            wanted (str): The desired aggregation operation.

        Returns:
            str: The constructed query with the aggregation operation.

        Raises:
            ValueError: If the specified aggregation operation is not recognized.
        """
        # Helper_query will be targeted specifically for performing aggregation functions later on
        helper_query = self.replace_variables_with_subsets(self.aggregation_condition)
        if self.aggregation == 'MIN':
            query = f'''min({helper_query})'''
        elif self.aggregation == 'AVG':
            query = f'''avg({helper_query})'''
        elif self.aggregation == 'MAX':
            query = f'''max({helper_query})'''
        elif self.aggregation == 'SUM':
            query = f'''sum({helper_query})'''
        elif self.aggregation == 'COUNT':
            query = f'''count({helper_query})'''
        else:
            raise ValueError("Specified aggregation operation not recognized.")
        return query
        
    def set_format(self, output_format):
        """
        Sets the output format for the datacube query.

        Parameters:
            output_format (str): The desired output format.

        Returns:
            Datacube: Returns the instance itself for method chaining.

        Raises:
            TypeError: If output_format is not a string.
            ValueError: If the specified output format is not supported.
        """
        if not isinstance(output_format, str):
            raise TypeError("Value entered must be a string.")
        if not (output_format in ['PNG', 'CSV', 'JPEG']):
            raise ValueError("Entered format doesn't exist")
        self.format = output_format
        return self
    
    def return_format(self):
        """
        Determines the format for the output based on the configured settings of the datacube.

        Returns:
            str: A string indicating the desired output format for the WCPS query.

        Example:
            >>> output_format = datacube.return_format()
        """
        if self.format == 'CSV':
            query = "text/csv"
        elif self.format == 'PNG':
            query = "image/png"
        elif self.format == 'JPEG': 
            query = "image/jpeg"
        return query
    
    def encode(self, operation):
        """
        Specifies the encoding operation to be applied to the output of the query.

        Parameters:
            operation (str): A string representing the encoding function, such as "encode".

        Returns:
            self: Returns the instance itself, allowing for method chaining.

        Example:
            >>> datacube.encode("
                switch 
                    case $c = 99999 
                        return {red: 255; green: 255; blue: 255} 
                    case 18 > $c
                        return {red: 0; green: 0; blue: 255} 
                    case 23 > $c
                        return {red: 255; green: 255; blue: 0} 
                    case 30 > $c
                        return {red: 255; green: 140; blue: 0} 
                    default return {red: 255; green: 0; blue: 0}
            ")
        """
        # Ensure the operation is a string, convert if not
        if not isinstance(operation, str):
            operation = str(operation)
        # Ensure all variables used in the operation are recognized by the datacube    
        if self.get_all_var_names(operation) != None:
            self.do_vars_exist(operation)
        self.encode_as = operation
        return self
    
    def construct_query(self):
        """
        Constructs a WCPS query based on the configured settings of the datacube.

        Returns:
            str: The constructed WCPS query.
        """
        query = '''for '''
        for var in self.variables:
            if isinstance(var, Coverage):
                query += f'${var.var_name} in ({",".join(var.coverage_names)})\n'
            else:
                query += (var + '\n')
        
        # Check for the usage of 'where' predicate. If it's None, skip it and put return to our query
        if self.filter != None:
            query += f'''where {self.filter_condition}\n'''
        query += f'''return \n'''
        
        # Check if any of the aggregation functions were used. If they were, add them to the query and return.
        if self.aggregation != None:
            query += self.aggregate_data()
            return query
        
        # Check if the encoding conditions were specified. If they were, add them to 'return'
        if self.encode_as != None:
            helper_query = self.replace_variables_with_subsets(self.encode_as)
        # Encoding condition wasn't specified, so check transformation operation
        elif self.transformation != None:
            helper_query = self.replace_variables_with_subsets(self.transformation)
        # Transformation wasn't used as well, so just return a variable with the corresponding subset
        elif self.switch_str != None:
            helper_query = self.switch_str
        else:
            helper_query = self.replace_variables_with_subsets()
        
        # If the format was specified, write encode() to the query
        if self.format != None: # Check whether the format was specified
            query += f'''encode({helper_query}, "{self.return_format()}")'''
        # If the encoding or data transformation were used, include encode()
        elif self.encode_as != None or self.transformation != None:
            query += f'''encode({helper_query}, "text/csv")'''
        else:
            query += f'''{helper_query}'''
        return query
        
    def execute(self):
        """
        Executes the constructed WCPS query and processes the response based on the specified format.

        Returns:
            str or list: Depending on the output format, returns either a string or a list of processed data.
        """
        wcps_query = self.construct_query()
        response = self.dbc.send_query(wcps_query)
        if self.format == 'CSV':
            data = byte_to_list(response.content) 
            self.reset()
            return data
        elif self.format == 'PNG':
            self.reset()
            return response.content
        elif self.format == 'JPEG':
            self.reset()
            return response.content
        else:
            self.reset()
            data = byte_to_list(response.content) 
            return data

    def add_coverages(self, *coverages):
        """
        Adds multiple coverages together and returns the result as a new coverage.

        Parameters:
            *coverages (Coverage): Variable number of coverage objects to add.

        Returns:
            Coverage: An expression representing the addition of the coverages.
        """
        if len(coverages) < 2:
            raise ValueError("At least two coverages are required for addition.")

        # Construct the query expression for the addition of coverages
        query_parts = [f'${cov.variable_name} in ({cov.coverage_names[0]})' for cov in coverages]
        query_vars = [f'${cov.variable_name}' for cov in coverages]
        query_expr = ',\n'.join(query_parts)

        # Construct the final query including the encoding part
        final_query = f'For\n{query_expr}\nreturn\nencode({" + ".join(query_vars)}, "text/csv")'

        # Create a new coverage representing the addition
        result = Coverage([], f'c{len(self.variables) + 1}')  # Adjust this line according to your Coverage class

        return result, final_query

    def subtract_coverages(self, *coverages):
        """
        Subtracts multiple coverages and returns the result as a new coverage.

        Parameters:
            *coverages (Coverage): Variable number of coverage objects to subtract.

        Returns:
            Coverage: An expression representing the subtraction of the coverages.
        """
        if len(coverages) < 2:
            raise ValueError("At least two coverages are required for subtraction.")

        # Construct the query expression for the subtraction of coverages
        query_parts = [f'${cov.variable_name} in ({cov.coverage_names[0]})' for cov in coverages]
        query_vars = [f'${cov.variable_name}' for cov in coverages]
        query_expr = ',\n'.join(query_parts)

        # Construct the final query including the encoding part
        final_query = f'For\n{query_expr}\nreturn\nencode({" - ".join(query_vars)}, "text/csv")'

        # Create a new coverage representing the subtraction
        result = Coverage([], f'c{len(self.variables) + 1}')  # Adjust this line according to your Coverage class

        return result, final_query

    def multiply_coverages(self, *coverages):
        """
        Multiplies multiple coverages together and returns the result as a new coverage.

        Parameters:
            *coverages (Coverage): Variable number of coverage objects to multiply.

        Returns:
            Coverage: An expression representing the multiplication of the coverages.
        """
        if len(coverages) < 2:
            raise ValueError("At least two coverages are required for multiplication.")

        # Construct the query expression for the multiplication of coverages
        query_parts = [f'${cov.variable_name} in ({cov.coverage_names[0]})' for cov in coverages]
        query_vars = [f'${cov.variable_name}' for cov in coverages]
        query_expr = ',\n'.join(query_parts)

        # Construct the final query including the encoding part
        final_query = f'For\n{query_expr}\nreturn\nencode({" * ".join(query_vars)}, "text/csv")'

        # Create a new coverage representing the multiplication
        result = Coverage([], f'c{len(self.variables) + 1}')  # Adjust this line according to your Coverage class

        return result, final_query

    def divide_coverages(self, *coverages):
        """
        Divides multiple coverages and returns the result as a new coverage.

        Parameters:
            *coverages (Coverage): Variable number of coverage objects to divide.

        Returns:
            Coverage: An expression representing the division of the coverages.
        """
        if len(coverages) < 2:
            raise ValueError("At least two coverages are required for division.")

        # Construct the query expression for the division of coverages
        query_parts = [f'${cov.variable_name} in ({cov.coverage_names[0]})' for cov in coverages]
        query_vars = [f'${cov.variable_name}' for cov in coverages]
        query_expr = ',\n'.join(query_parts)

        # Construct the final query including the encoding part
        final_query = f'For\n{query_expr}\nreturn\nencode({" / ".join(query_vars)}, "text/csv")'

        # Create a new coverage representing the division
        result = Coverage([], f'c{len(self.variables) + 1}')  # Adjust this line according to your Coverage class

        return result, final_query
    
class Coverage:
    def __init__(self, coverage_names, variable_name):
        """
        Creates a Coverage instance with the provided coverage names and variable name.

        Parameters:
            coverage_names (list): A list of coverage names.
            variable_name (str): The name of the variable associated with the coverage.

        Example:
            >>> cov = Coverage(["temperature", "humidity"], "var1")
        """
        self.coverage_names = coverage_names
        self.variable_name = variable_name

    def __add__(self, other):
        """
        Defines addition operation between two Coverage instances.

        Parameters:
            other (Coverage): Another Coverage instance to be added.

        Returns:
            BinaryOperation: Represents the addition operation between two Coverages.

        Raises:
            TypeError: If the other operand is not a Coverage instance.
        """
        if isinstance(other, Coverage):
            return BinaryOperation(self, other, '+')
        else:
            raise TypeError("Unsupported operand type(s) for +: '{}' and '{}'".format(
                type(self).__name__, type(other).__name__))

    def __sub__(self, other):
        """
        Defines subtraction operation between two Coverage instances.

        Parameters:
            other (Coverage): Another Coverage instance to be subtracted.

        Returns:
            BinaryOperation: Represents the subtraction operation between two Coverages.

        Raises:
            TypeError: If the other operand is not a Coverage instance.
        """
        if isinstance(other, Coverage):
            return BinaryOperation(self, other, '-')
        else:
            raise TypeError("Unsupported operand type(s) for -: '{}' and '{}'".format(
                type(self).__name__, type(other).__name__))

    def __mul__(self, other):
        """
        Defines multiplication operation between two Coverage instances.

        Parameters:
            other (Coverage): Another Coverage instance to be multiplied.

        Returns:
            BinaryOperation: Represents the multiplication operation between two Coverages.

        Raises:
            TypeError: If the other operand is not a Coverage instance.
        """
        if isinstance(other, Coverage):
            return BinaryOperation(self, other, '*')
        else:
            raise TypeError("Unsupported operand type(s) for *: '{}' and '{}'".format(
                type(self).__name__, type(other).__name__))

    def __truediv__(self, other):
        """
        Defines division operation between two Coverage instances.

        Parameters:
            other (Coverage): Another Coverage instance to be divided.

        Returns:
            BinaryOperation: Represents the division operation between two Coverages.

        Raises:
            TypeError: If the other operand is not a Coverage instance.
        """
        if isinstance(other, Coverage):
            return BinaryOperation(self, other, '/')
        else:
            raise TypeError("Unsupported operand type(s) for /: '{}' and '{}'".format(
                type(self).__name__, type(other).__name__))


class BinaryOperation:
    def __init__(self, lhs, rhs, operator):
        """
        Initializes a BinaryOperation instance.

        Parameters:
            lhs (Coverage): The left-hand side Coverage instance.
            rhs (Coverage): The right-hand side Coverage instance.
            operator (str): The operator symbol representing the operation.

        Example:
            >>> operation = BinaryOperation(Coverage(["temp1"], "var1"), Coverage(["temp2"], "var2"), '+')
        """
        self.lhs = lhs
        self.rhs = rhs
        self.operator = operator