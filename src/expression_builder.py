# The Variable class represents a variable in mathematical expressions.
class Variable:
    # Initializes a Variable with a given name.
    def __init__(self, name):
        self.name = name
        
    # Adds a dollar sign prefix to the variable name.
    def with_prefix(self):
        return Variable(f"${self.name}")

    # Generates a string representing a greater-than comparison between this variable and another value.
    def greater_than(self, other):
        return f"${self.name} > {other}"

    # Generates a string representing a less-than comparison between this variable and another value.
    def less_than(self, other):
        return f"${self.name} < {other}"

    # Returns the logical AND operator as a string.
    def and_(self):
        return " and "
    
    # Performs addition between this variable and another variable or scalar.
    def add(self, other):
        return f"{self.name} + {other}"

    # Performs subtraction between this variable and another variable or scalar.
    def subtract(self, other):
        return f"{self.name} - {other}"

    # Performs multiplication between this variable and another variable or scalar.
    def multiply(self, other):
        return f"{self.name} * {other}"

    # Performs division between this variable and another variable or scalar.
    def divide(self, other):
        return f"{self.name} / {other}"

# The Scalar class represents a numerical scalar value.
class Scalar:
    # Initializes a Scalar with a given value.
    def __init__(self, value):
        self.value = value

    # Returns the string representation of the scalar value.
    def __str__(self):
        return str(self.value)
    
    # Performs addition between this scalar and another scalar.
    def add(self, other):
        return f"{self.value} + {other}"

    # Performs subtraction between this scalar and another scalar.
    def subtract(self, other):
        return f"{self.value} - {other}"

    # Performs multiplication between this scalar and another scalar.
    def multiply(self, other):
        return f"{self.value} * {other}"

    # Performs division between this scalar and another scalar.
    def divide(self, other):
        return f"{self.value} / {other}"