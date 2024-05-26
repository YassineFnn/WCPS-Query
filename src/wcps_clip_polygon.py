import math

class ClipPolygon:
    """
    Represents a polygon for clipping in a WCPS query.
    """

    def __init__(self):
        """
        Initializes a new ClipPolygon instance.
        """
        self.polygon = []

    def add_point(self, lat, long):
        """
        Adds a point to the POLYGON in the WCPS query.

        Parameters:
            lat (float): The latitude of the point.
            long (float): The longitude of the point.

        Returns:
            ClipPolygon: The current instance of ClipPolygon.
        """
        point_str = "{:.4f} {:.4f}".format(lat, long)
        self.polygon.append(point_str)
        return self

    def clear_polygon(self):
        """
        Clears all points from the polygon.
        """
        self.polygon = []

    def is_valid_polygon(self):
        """
        Checks if the polygon is valid, i.e., it has at least three points and forms a closed loop.

        Returns:
            bool: True if the polygon is valid, False otherwise.
        """
        return len(self.polygon) >= 3

    def calculate_polygon_area(self):
        """
        Calculates the area of the polygon using the shoelace formula.

        Returns:
            float: The area of the polygon.
        """
        if not self.is_valid_polygon():
            raise ValueError("Invalid polygon: It must have at least three points and form a closed loop.")

        area = 0
        n = len(self.polygon)
        for i in range(n):
            lat1, lon1 = map(float, self.polygon[i].split())
            lat2, lon2 = map(float, self.polygon[(i + 1) % n].split())
            area += (lon1 + lon2) * (lat2 - lat1)
        return abs(area) / 2

    def is_point_inside_polygon(self, lat, lon):
        """
        Checks if a given point is inside the polygon.

        Parameters:
            lat (float): The latitude of the point.
            lon (float): The longitude of the point.

        Returns:
            bool: True if the point is inside the polygon, False otherwise.
        """
        if not self.is_valid_polygon():
            raise ValueError("Invalid polygon: It must have at least three points and form a closed loop.")

        x = lat
        y = lon
        inside = False
        n = len(self.polygon)
        p1x, p1y = map(float, self.polygon[0].split())
        for i in range(n + 1):
            p2x, p2y = map(float, self.polygon[i % n].split())
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside

    def to_clip_expression(self):
        """
        Generates the clip expression for the POLYGON.

        Returns:
            str: The clip expression for the POLYGON.
        """
        if not self.is_valid_polygon():
            raise ValueError("Invalid polygon: It must have at least three points and form a closed loop.")
            
        polygon_str = ", ".join(self.polygon)  # Joining the points with commas
        clip_expression = f"POLYGON(({polygon_str}))"
        return clip_expression

    def to_geojson(self):
        """
        Converts the polygon to GeoJSON format.

        Returns:
            dict: The GeoJSON representation of the polygon.
        """
        if not self.is_valid_polygon():
            raise ValueError("Invalid polygon: It must have at least three points and form a closed loop.")

        coordinates = [[float(lon), float(lat)] for lat, lon in [point.split() for point in self.polygon]]
        # Append the first coordinate at the end to close the loop
        coordinates.append(coordinates[0])

        geojson = {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [coordinates]
            },
            "properties": {}
        }
        return geojson

    def rotate_polygon(self, angle, center_lat, center_lon):
        """
        Rotates the polygon by a specified angle around a given center point.

        Parameters:
            angle (float): The rotation angle in degrees.
            center_lat (float): The latitude of the center point.
            center_lon (float): The longitude of the center point.
        """
        angle_rad = math.radians(angle)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)
        center_x, center_y = center_lat, center_lon
        for i in range(len(self.polygon)):
            lat, lon = map(float, self.polygon[i].split())
            # Translate coordinates to be relative to the center
            translated_x = lat - center_x
            translated_y = lon - center_y
            # Perform rotation around the center point
            rotated_x = translated_x * cos_angle - translated_y * sin_angle
            rotated_y = translated_x * sin_angle + translated_y * cos_angle
            # Translate back to the original coordinates and update polygon point
            self.polygon[i] = "{:.4f} {:.4f}".format(rotated_x + center_x, rotated_y + center_y)

    def scale_polygon(self, factor):
        """
        Scales the polygon by a given factor around a specified center point.

        Parameters:
            factor (float): The scaling factor.
            center_lat (float): The latitude of the center point.
            center_lon (float): The longitude of the center point.
        """
        for i in range(len(self.polygon)):
            lat, lon = map(float, self.polygon[i].split())
            scaled_x = lat * factor
            scaled_y = lon * factor
            self.polygon[i] = "{:.4f} {:.4f}".format(scaled_x, scaled_y)