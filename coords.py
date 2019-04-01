import geopy
import json
import urllib.request


# METHODES DE TRAITEMENT DES LONGITUDES/LATITUDES AFFICHEES DANS UN TWEET
# Ces méthodes font la moyennes des valeurs du "polygone" de la localisation d'un tweet
# =============================================================================
def getLongAndLat(listeCouplesCoord):
    """
    Parse the list that was entered as a param into two lists, to separate the
    coordonates

    Parameters
    ----------
    list : listeCouplesCoord
        a list that contains lists of coords
    Returns
    -------
        tuple(list,list) :
            a tuple of lists, longitude and latitude
    """ 
    listeLongitude = []
    listeLatitude = []
    for couple in listeCouplesCoord:
        listeLongitude.append(couple[0])
        listeLatitude.append(couple[1])
    return (listeLongitude,listeLatitude)

def moyList(list):
    """
    calculate the mean of the list

    Parameters
    ----------
    list : list
        a list that contains integer/float
    Returns
    -------
        numeric :
            the list's mean
    """ 
    return (sum(list)/len(list))


def centrePolygone(list_Longitude, list_Latitude):
    """
    determine the center of the polygon from its coordinate

    Parameters
    ----------
    list(numeric) : list_Longitude
        list of all its longitudes
    list(numeric) : list_Latitude
        list of all its latitude
    Returns
    -------
        list[numeric, numeric]:
            a list of the mean of the longitudes and the mean of the latitudes
    """ 
    return [moyList(list_Longitude), moyList(list_Latitude)]

def is_in_polygon(lat,long,polygonCity):
    """
    Determine if a coordinate is in a polygon of a city

    Parameters
    ----------
    numeric : lat
        latitude of the point
    numeric : long
        longitude of the point
    list[tuple(coordinates)] : polygonCity
        a list of coordinates that circle the city
    Returns
    -------
        boolean:
            a boolean, true if the point is in the polygon, false otherwise
    """ 
    #création des différentes arêtes composant le polygone (en "joignant" les sommets 2 à 2)
    #le premier sommet et le dernier sont les mêmes, donc inutile de les lier entre eux
    nombre_intersections = 0
    for i,coord in enumerate(polygonCity[:-1]):
        xA = polygonCity[i][0]
        yA = polygonCity[i][1]
        xB = polygonCity[i+1][0]
        yB = polygonCity[i+1][1]
        # voir explication de l'algorithme sur http://alienryderflex.com/polygon/
        # Pour résumer, il faut compter les intersections entre les aretes du polygone et la droite horizontale passant
        # par les coordonnées testées, en ne prenant en compte que les aretes qui au moins un sommet plus à gauche que
        # la longitude (l'abscisse X) du point testé. Si le nombre d'intersections est impair, alors le point est dans le polygone.
        # On compte une intersection seulement lorsqu'un des sommets est strictement en dessous de la droite horizontale, et l'autre
        # sommet au dessus ou sur la droite.

        #On teste si l'arete est à gauche du point :
        if xA < long or xB < long:
            #On teste si l'un des deux points est strictement en dessous, et que l'autre est au dessus ou sur la droite :
            if (yA  < lat and yB >= lat) or (yB < lat and yA >= lat):
                nombre_intersections+=1
    #Si le nombre d'intersections est impair, alors le point est dans le polygone. Sinon, il est en dehors.
    if nombre_intersections % 2 == 1:
        return True
    else:
        return False

def get_address(lat,long):
    """
    Ask an API for the exact address of coordinates

    Parameters
    ----------
    numeric : lat
        latitude of the point
    numeric : long
        longitude of the point
    Returns
    -------
        str:
            the address of the coordinates
    """     
    geolocator = geopy.Nominatim(user_agent="monAppTwitter")
    location = geolocator.reverse(str(lat)+','+str(long),addressdetails=True)
    return location.raw

def get_polygon_city(cityName,country):
    """
    Ask an API for the coordinates that circle a city

    Parameters
    ----------
    str : cityName
        Name of the city
    str : country
        name of the country
    Returns
    -------
        list(tuple(coordinates)):
            a list of coordinates
    """     
    geolocator = geopy.Nominatim(user_agent="monAppTwitter")
    location = geolocator.geocode(cityName+","+country)
    osm_id = location.raw["osm_id"]
    #Turin : 44880
    #Grenoble : 80348
    #Annecy : 102480
    page = urllib.request.urlopen(
        'http://polygons.openstreetmap.fr/get_geojson.py?id='+str(osm_id)+'&params=0')
    cityCoords = json.loads(str(page.read())[2:-3])["geometries"][0]["coordinates"][0][0]
    return cityCoords

def getCenterCoords(ville,pays):
    """
    Ask an API for the coordinates that are at the center of a city

    Parameters
    ----------
    str : ville
        Name of the city
    str : pays
        name of the country
    Returns
    -------
        tuple(coordinates):
            a tuple of coordinates
    """  
    geolocator = geopy.Nominatim(user_agent="monAppTwitter")
    location = geolocator.geocode(ville+","+pays)
    return [location.latitude, location.longitude]

