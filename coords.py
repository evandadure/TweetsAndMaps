import geopy
import json
import urllib.request


# METHODES DE TRAITEMENT DES LONGITUDES/LATITUDES AFFICHEES DANS UN TWEET
# Ces méthodes font la moyennes des valeurs du "polygone" de la localisation d'un tweet
# =============================================================================
def getLongAndLat(listeCouplesCoord):
    listeLongitude = []
    listeLatitude = []
    for couple in listeCouplesCoord:
        listeLongitude.append(couple[0])
        listeLatitude.append(couple[1])
    return (listeLongitude,listeLatitude)

def moyList(list):
    return (sum(list)/len(list))


def centrePolygone(list_Longitude, list_Latitude):
    return [moyList(list_Longitude), moyList(list_Latitude)]

def is_in_polygon(lat,long,polygonCity):
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
    geolocator = geopy.Nominatim(user_agent="monAppTwitter")
    location = geolocator.reverse(str(lat)+','+str(long),addressdetails=True)
    return location.raw

def get_polygon_city(cityName,country):
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
    geolocator = geopy.Nominatim(user_agent="monAppTwitter")
    location = geolocator.geocode(ville+","+pays)
    return [location.latitude, location.longitude]





#
#
#
# listeCoords = [[45.889751, 6.135465],[45.363139,5.591075],[46.9202614, 7.1570201]]
# m = create_map()
# for coords in listeCoords:
#     add_marker(m,coords,[])
#
# m.save('map.html')






# folium.Marker([45.9202614, 6.1570201],
#               popup='<strong>Testzz</strong><ul><li>test</li><li>test2</li></ul>',
#               tooltip=tooltip,
#               icon=logoTwitter).add_to(m)

#
# # Vega data
# vis = os.path.join('data', 'vis.json')
#
# Geojson Data
# overlay = os.path.join('data', 'overlay.json')
#
#
# # Geojson overlay (encadrement d'une ville à partir de son polygone de coordonnées
# folium.GeoJson(overlay, name='paris').add_to(m)




# folium.Marker([42.333600, -71.109500],
#               popup='<strong>Location Two</strong>',
#               tooltip=tooltip,
#               icon=folium.Icon(icon='cloud')).add_to(m),
# folium.Marker([42.377120, -71.062400],
#               popup='<strong>Location Three</strong>',
#               tooltip=tooltip,
#               icon=folium.Icon(color='purple')).add_to(m),
# folium.Marker([42.374150, -71.122410],
#               popup='<strong>Location Four</strong>',
#               tooltip=tooltip,
#               icon=folium.Icon(color='green', icon='leaf')).add_to(m),
# folium.Marker([42.375140, -71.032450],
#               popup='<strong>Location Five</strong>',
#               tooltip=tooltip,
#               icon=logoIcon).add_to(m),
# folium.Marker([42.315140, -71.072450],
#               popup=folium.Popup(max_width=450).add_child(folium.Vega(json.load(open(vis)), width=450, height=250))).add_to(m)
#
# # Circle marker
# folium.CircleMarker(
#     location=[42.466470, -70.942110],
#     radius=50,
#     popup='My Birthplace',
#     color='#428bca',
#     fill=True,
#     fill_color='#428bca'
# ).add_to(m)
