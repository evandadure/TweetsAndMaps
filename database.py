import mysql.connector
from datetime import datetime, timedelta

# CONNECTION TO THE DATABASE
# =============================================================================
# host = "tp-epu.univ-savoie.fr",
# port = "3308",
# user = "personma",
# passwd = "rca8v7gd",
# database = "personma"
# =============================================================================

def connectMySQLDB(host,port,user,passwd,database):
    mydb = mysql.connector.connect(
    host=host,
    port=port,
    user=user,
    passwd=passwd,
    database=database
    )
    return (mydb,mydb.cursor())

def setDateTime(dateTweet):
    """
    Fonction qui crée un datetime à partir d'une string de date (exemple "21/08/18"), et d'une string d'heure (exemple "13:37")
    Parametres :
        - date : String de la date
        - heure : String de l'heure
    Retourne :
        d : la date (et son heure) dans le type datetime
    """
    monthsDic  = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
    dateToString = dateTweet[8:10]+"/"+monthsDic[dateTweet[4:7]]+"/"+dateTweet[-2:]
    d = datetime.strptime(dateToString,"%d/%m/%y")
    h = dateTweet[dateTweet.find(':')-2:dateTweet.find(':')]
    m = dateTweet[dateTweet.find(':')+1:dateTweet.find(':')+3]
    d = d.replace(hour=int(h),minute=int(m))
    d = d + timedelta(hours=1)
    return d


def addTweet(mydb, mycursor,numero_tweet, created_at, text, user_id, user_name, screen_name, latitude, longitude, searched_keyword, nearest_city):
    sql = "INSERT INTO tweet (numero_tweet, created_at, text, user_id, user_name, screen_name, \
        latitude, longitude, searched_keyword, nearest_city) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (numero_tweet, created_at, text, user_id, user_name, screen_name, latitude, longitude, searched_keyword, nearest_city)
    mycursor.execute(sql, val)
    mydb.commit()

def addWord(mydb, mycursor,word):
    sql = "REPLACE INTO word (label) VALUES ('"+word+"')"
    mycursor.execute(sql)
    mydb.commit()

def addCity(mydb, mycursor,city):
    sql = "REPLACE INTO city (city_name) VALUES ('"+city+"')"
    mycursor.execute(sql)
    mydb.commit()

def addKeywords(mydb, mycursor,numero_tweet, city, wordList):
    addCity(city)
    for word in wordList:
        addWord(word)
        sql = "REPLACE INTO keyword (numero_tweet,city_name,label) VALUES (%s, %s, %s)"
        val = (numero_tweet, city, word)
        mycursor.execute(sql,val)
        mydb.commit()

def deleteQuestionMarksOnly(mydb, mycursor):
    for i in range(100):
        str = ""
        for j in range(i):
            str += "?"
        sql = "DELETE FROM keyword WHERE label LIKE '"+str+"';"
        mycursor.execute(sql)
        sql = "DELETE FROM word WHERE label LIKE '"+str+"';"
        mycursor.execute(sql)
        mydb.commit()