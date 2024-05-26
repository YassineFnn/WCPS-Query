def byte_to_list(byte_str):
    """
    Converts a byte string into a list of floats. Useful for parsing numeric data returned from a server.

    Parameters:
        byte_str (bytes): The byte string to be converted.

    Returns:
        list of float: A list of floats derived from the byte string.

    Example:
        >>> byte_to_list(b'1.0,2.0,3.0')
        [1.0, 2.0, 3.0]
    """
    decoded_str = byte_str.decode('utf-8')  # decode the byte string
    # Split the string by whitespace and remove any empty strings
    str_list = filter(None, decoded_str.split())
    # Convert the list of strings to floats
    num_list = []
    for num_str in str_list:
        try:
            num_list.append(float(num_str))
        except ValueError:
            pass  # Ignore non-numeric values
    return num_list