import pandas as pd
import googlemaps
import geocoder
from shapely.geometry import Point
from geopandas import GeoDataFrame
from geojsonio import display


class geo19s():

    # Google Maps API authentication
    gmaps = googlemaps.Client(key='[KEY]')

    def __init__(self, name=None, filename=None):
        if filename:
            self.data = pd.read_csv(filename)
        else:
            # Create an empty dataframe with address, latitude and longitude
            columns = ['Address', 'Lat', 'Long']
            self.data = pd.DataFrame(columns=columns)

        if name:
            # Set a name for our data
            self.name = name

    def address_to_coords(self, filename=None, tags=None):
        """
        If we only have the address, we obtain the (lat, long) coordinates
        using geocoder.
        """
        if filename:
            temp = pd.read_csv(filename)
            if tags:
                self.data['Coordinates'] = [Point(xy) for xy in zip(
                    self.data[tags[1]], self.data[tags[0]])]
            else:
                self.data['Lat'] = temp['Address'].apply(
                    geocoder.google).apply(lambda x: x.lat)
                self.data['Long'] = temp['Address'].apply(
                    geocoder.google).apply(lambda x: x.lng)
                self.data['Coordinates'] = [
                    Point(xy) for xy in zip(self.data.Long, self.data.Lat)]
        else:
            try:
                if tags:
                    self.data['Lat'] = self.data[tags[0]].apply(
                        geocoder.google).apply(lambda x: x.lat)
                    self.data['Long'] = self.data[tags[1]].apply(
                        geocoder.google).apply(lambda x: x.lng)
                    self.data['Coordinates'] = [Point(xy) for xy in zip(
                        self.data[tags[1]], self.data[tags[0]])]
                else:
                    self.data['Lat'] = self.data['Address'].apply(
                        geocoder.google).apply(lambda x: x.lat)
                    self.data['Long'] = self.data['Address'].apply(
                        geocoder.google).apply(lambda x: x.lng)
                    self.data['Coordinates'] = [
                        Point(xy) for xy in zip(self.data.Long, self.data.Lat)]
            except:
                print("Error trying to convert an address to coordinates.")

    def latlong_to_coords(self, filename=None, tags=None):
        """
        If we only already hay the latitude and longitude, compute
        (lat, long) coordinates using geocoder.
        """
        if filename:
            temp = pd.read_csv(filename)
            if tags:
                self.data['Coordinates'] = [Point(xy) for xy in zip(
                    self.data[tags[1]], self.data[tags[0]])]
            else:
                self.data['Coordinates'] = [
                    Point(xy) for xy in zip(self.data.Long, self.data.Lat)]
        else:
            try:
                if tags:
                    self.data['Coordinates'] = [Point(xy) for xy in zip(
                        self.data[tags[1]], self.data[tags[0]])]
                else:
                    self.data['Coordinates'] = [
                        Point(xy) for xy in zip(self.data.Long, self.data.Lat)]
            except:
                print("Error trying to convert an lat/long to coordinates.")

    def get_geo(self):
        return(list(self.data['Coordinates']))

    def get_name(self):
        return self.name

    def get_address(self):
        return self.data.entidad

    def get_gdf(self):
        crs = {'init': 'epsg:4326'}
        return GeoDataFrame(self.get_address(), crs=crs, geometry=self.get_geo())

    def visualize(self):
        geovis = self.get_gdf()
        display(geovis.to_json())


if __name__ == "__main__":
    geo19s = geo19s(name="Real Providencia",
                    filename="Derrumbe-datos.gob.mx.csv")
    geo19s.latlong_to_coords(tags=["latitud", "longitud"])
    geo19s.visualize()
