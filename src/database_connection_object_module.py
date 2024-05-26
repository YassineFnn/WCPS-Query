import requests

class DatabaseConnection:
    # initalizing our dbc by providing it with the service endpoint, from which we can get a datacube
    def __init__(self, url):
        """
        Initializes a new dbc instance which is used to manage connections and send queries to a WCPS server.

            >>> database_connection = dbc("https://ows.rasdaman.org/rasdaman/ows")
        """
        if not isinstance(url, str):
            raise TypeError("Value entered must be a string.")
        self.server_url = url
    
    def send_query(self, wcps_query):
        """
        Sends a WCPS query to the server and retrieves the response.

        Returns:Response: A response object from the requests library containing the server's response to the query.


        """
        if not isinstance(wcps_query, str):
            raise TypeError("Value entered must be a string.")
        # getting a response from the server
        try:
            # 'verify=False' is used to skip SSL certificate verification;
            response = requests.post(self.server_url, data = {'query': wcps_query}, verify = False)
            if response.status_code == 200:
                return response
            else:
                raise ValueError("Not correct query")
        except:
            raise Exception("Something is wrong...")
         # General exception handling to catch potential issues like network 
