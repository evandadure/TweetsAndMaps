import folium
import coords
import os
try:
    import json
except ImportError:
    import simplejson as json


# This module contains functions that are creating and editing a map. The Folium module is used to create and modify
# an HTML file using the Javascript libraries Leaflet.JS and d3js. The map is taken from OpenStreetMap and is firstly
# empty. You can then add some cursors (with some information displayed on click), and some colorful polygons.

def create_map():
    """
    Creates and return a Folium Map object
    ----------
    Parameters :
        No parameters.
    Returns :
        - folium.Map : a Folium's map object, centered on France by default and zoomed to see all the country
    """

    return folium.Map(location=[47.07421, 2.4142873], zoom_start=6)

def add_marker(map,latitude,longitude,username,screenname,text,date, adr_display):
    """
    Adds a tweet marker on a map, which will display a description when clicked on.
    ----------
    Parameters :
        - map (folium.folium.Map) : a map
        - latitude (float) : the latitude of the marker
        - longitude (float) : the longitude of the marker
        - username (str) : the twitter username of the tweet's user
        - screenname (str) : the twitter screenname of the tweet's user
        - text (str) : the tweet's text
        - date (str) : the tweet's date
        - adr_display (str) : the address description (containing Country, County, City, etc...)
    Returns :
        No return
    """
    # As an HTML page will be generated, we use HTML tags to make our description look better.
    description = "<strong>"+username+"(@"+screenname+")</strong> \
                </br><i>"+date+"</i> \
                </br>"+text+"</br> \
                </br></br>"+adr_display
    # The main information about the marker
    folium.Marker(
          location=[latitude,longitude],
          popup=description,
          tooltip='Voir + d\'infos').add_to(map),

def displayAllTweets(mycursor,map, city="",searched_word=""):
    """
    Adds a marker for each tweets from the database in their exact location. A city can be specified to search only tweets which
    have this city as their county, and a searched_word can be specified to search only tweets containing this string.
    ----------
    Parameters :
        - mycursor (mysql.connector.cursor.MySQLCursor) : a cursor of the database connection
        - map (folium.folium.Map) : a map
        - city (str) : the tweet's city
        - searched_word (str) : an expression that should be in the displayed tweets.
    Returns :
        No return
    """
    mycursor.execute("SELECT * FROM tweet WHERE nearest_city LIKE '%"+city+"%' AND text LIKE '%"+searched_word+"%'")
    myresult = mycursor.fetchall()
    for line in myresult:
        #If there is a location (here we just try to check if there is a latitude):
        if line[6] != "0":
            addr_infos = coords.get_address(line[6], line[7])
            add_marker(map, float(line[6]), float(line[7]), line[4], line[5], line[2],
                              str(line[1]), addr_infos["display_name"])

def displayAllTweetsCenter(mycursor,map, city="",country="",searched_word=""):
    """
    Adds a marker for each tweets from the database in one "central" location of the nearest city of the tweet's location. A city
    can be specified to search only tweets which have this city as their county, and a searched_word can be specified
    to search only tweets containing this string.
    ----------
    Parameters :
        - mycursor (mysql.connector.cursor.MySQLCursor) : a cursor of the database connection
        - map (folium.folium.Map) : a map
        - city (str) : the tweet's city
        - searched_word (str) : an expression that should be in the displayed tweets.
    Returns :
        No return
    """
    mycursor.execute("SELECT * FROM tweet WHERE nearest_city LIKE '%"+city+"%' AND text LIKE '%"+searched_word+"%'")
    myresult = mycursor.fetchall()
    for line in myresult:
        #If there is a location (here we just check if there is a latitude):
        if line[6] != "0":
            #We're using a try/catch here because sometimes the location can't be found with Geopy's API, and we don't
            #want it to stop our program.
            try:
                addr_infos = coords.get_address(line[6], line[7])
                #We're using coords.getCenterCoords to get the center coordinates of a city.
                coordsCenterCity = coords.getCenterCoords(addr_infos["address"]["county"],addr_infos["address"]["country"])
                add_marker(map, coordsCenterCity[0], coordsCenterCity[1], line[4], line[5], line[2],
                              str(line[1]), addr_infos["address"]["county"])
            except:
                print("Couldn't find the address of the tweet", line[0])


def displayPolygonCity(map, city, country):
    """
    Adds a "city polygon" around a city on the map, by changing the JSON file data/overlay.json with the coordinates of a polygon
    surrounding the city
    ----------
    Parameters :
        - map (folium.folium.Map) : a map
        - city (str) : the tweet's city
        - country (str) : the tweet's country
    Returns :
        No return
    """
    #Gets the city polygon first
    coordsPolygon = coords.get_polygon_city(city,country)
    #Creates a JSON description containing all coordinates of the polygon
    data = {}
    data["type"] = "FeatureCollection"
    data["features"] = []
    data["features"].append({
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "LineString",
            "coordinates": coordsPolygon
        }
    })
    #Modifies the JSON file with this new JSON description
    with open('data/overlay.json', 'w') as outfile:
        json.dump(data, outfile)
    #Adds the city polygon from the JSON file on the map
    overlay = os.path.join('data', 'overlay.json')
    folium.GeoJson(overlay, name=city).add_to(map)