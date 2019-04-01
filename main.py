import database
import twitter_api
import displays

# print(type(only_located))
# time.sleep(80)

database.setDateTime("Mon Apr 01 17:09:19 +0000 2019")

Connexion à la base de données
mydb,mycursor = database.connectMySQLDB("localhost","3306","root","root","tp_twitterosm")

Sauvegarde des tweets (selon des critères) dans la BDD
twitter_api.saveTweets(mydb, mycursor,searched_word="", number_max=10000000,only_located=True,city="Grenoble",country="France",radius="60")

Création d'une map vierge
map = displays.create_map()

Affichage de tweets sur la map (d'après leur localisation)
displays.displayAllTweets(mycursor,map, city="",searched_word="avec")

Affichage de tweets sur la map (d'après la localisation du centre de la grande ville la plus proche)
displays.displayAllTweetsCenter(mycursor,map, city="",country="",searched_word="")

Affichage du polygone entourant une ville en particulier
displays.displayPolygonCity(map,"Grenoble","France")

Sauvegarde de la map dans le fichier map.html
map.save('map.html')

Suppression des mots et mots-clé contenant uniquement des points d'interrogations (à cause des caractères non reconnus par MySQL)
database.deleteQuestionMarksOnly(mydb, mycursor)

Affichage des 10 mots clés les plus utilisés dans les tweets d'une ville donnée :
database.mostUsedKeywords(mycursor,"Grenoble",10)
