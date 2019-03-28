import folium
import coords
import os
try:
    import json
except ImportError:
    import simplejson as json


def create_map():
    return folium.Map(location=[47.07421, 2.4142873], zoom_start=6)

def add_marker(map,latitude,longitude,username,screenname,text,date, adr_display):
    description = "<strong>"+username+"(@"+screenname+")</strong> \
                </br><i>"+date+"</i> \
                </br>"+text+"</br> \
                </br></br>"+adr_display
    folium.Marker(
          location=[latitude,longitude],
          popup=description,
          tooltip='Voir + d\'infos').add_to(map),

def displayAllTweets(mycursor,map, city="",searched_word=""):
    mycursor.execute("SELECT * FROM tweet WHERE nearest_city LIKE '%"+city+"%' AND searched_keyword LIKE '%"+searched_word+"%'")
    myresult = mycursor.fetchall()
    for line in myresult:
        #If there is a location (here we just try to check if there is a latitude):
        if line[6] != "0":
            addr_infos = coords.get_address(line[6], line[7])
            add_marker(map, float(line[6]), float(line[7]), line[4], line[5], line[2],
                              str(line[1]), addr_infos["display_name"])

def displayAllTweetsCenter(mycursor,map, city="",country="",searched_word=""):
    mycursor.execute("SELECT * FROM tweet WHERE nearest_city LIKE '%"+city+"%' AND searched_keyword LIKE '%"+searched_word+"%'")
    myresult = mycursor.fetchall()
    for line in myresult:
        #If there is a location (here we just try to check if there is a latitude):
        if line[6] != "0":
            try:
                addr_infos = coords.get_address(line[6], line[7])
                coordsCenterCity = coords.getCenterCoords(addr_infos["address"]["county"],addr_infos["address"]["country"])
                add_marker(map, coordsCenterCity[0], coordsCenterCity[1], line[4], line[5], line[2],
                              str(line[1]), addr_infos["address"]["county"])
            except:
                print("Couldn't find the address of the tweet", line[0])


def displayPolygonCity(map, city, country):
    coordsPolygon = coords.get_polygon_city(city,country)
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
    with open('data/overlay.json', 'w') as outfile:
        json.dump(data, outfile)

    overlay = os.path.join('data', 'overlay.json')
    folium.GeoJson(overlay, name=city).add_to(map)








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
