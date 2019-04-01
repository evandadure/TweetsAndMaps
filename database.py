import mysql.connector
from datetime import datetime, timedelta
import time

def connectMySQLDB(host,port,user,passwd,database):
    """
    Connects to your MySQL database.
    ----------
    Parameters :
        - host (str) : the host name (default is localhost)
        - port (str) : the port number (default with MySQL is 3306)
        - user (str) : the database user name (default is root)
        - passwd (str) : the database password (default is empty, I've set it to root)
        - database (str) : the name of your database
    Returns :
        - mydb (mysql.connector.connection.MySQLConnection) : the database connection
        - mycursor (mysql.connector.cursor.MySQLCursor) : a cursor of the connection
            (both are returned in a 2-tuple)
    """
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
    Function that converts the tweet default date format to a date format compatible with MySQL databases (Python datetime)
    For example, "Mon Apr 01 17:09:19 +0000 2019" will be converted in "2019-04-01 18:09:00" (We add one hour to the time
    because we have UTC+1 in France)
    ----------
    Parameters :
        - dateTweet (str) : the tweet's publication date (and time)
    Returns :
        - d (datetime.datetime) : a datetime object
    """
    monthsDic  = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
    # We're getting the day,month,year,hour and minute from the tweet time to create a new datetime
    dateToString = dateTweet[8:10]+"/"+monthsDic[dateTweet[4:7]]+"/"+dateTweet[-2:]
    d = datetime.strptime(dateToString,"%d/%m/%y")
    h = dateTweet[dateTweet.find(':')-2:dateTweet.find(':')]
    m = dateTweet[dateTweet.find(':')+1:dateTweet.find(':')+3]
    d = d.replace(hour=int(h),minute=int(m))
    # We add one hour to the time because we have UTC+1 in France
    d = d + timedelta(hours=1)
    return d


def addTweet(mydb, mycursor, tweet_number, created_at, text, user_id, user_name, screen_name, latitude, longitude, searched_keyword, nearest_city):
    """
    Adds a tweet in the database
    ----------
    Parameters :
        - mydb (mysql.connector.connection.MySQLConnection) : the database connection
        - mycursor (mysql.connector.cursor.MySQLCursor) : a cursor of the connection
        - tweet_number (str) : the tweet ID
        - created_at (datetime.datetime) : the tweet's publication date and hour
        - text (str) : the tweet's text
        - user_id (str) : the tweet's user ID
        - user_name (str) : the tweet's user name
        - screen_name (str) : the tweet's user screen name
        - latitude (float) : the latitude of the tweet's location
        - longitude (float) : the longitude of the tweet's location
        - searched_keyword (str) : searched_keyword of the tweet
        - nearest_city (str) : nearest_city of the tweet
    """
    print(type(user_id),type(latitude))
    time.sleep(8000)
    sql = "INSERT INTO tweet (numero_tweet, created_at, text, user_id, user_name, screen_name, \
        latitude, longitude, searched_keyword, nearest_city) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    val = (tweet_number, created_at, text, user_id, user_name, screen_name, latitude, longitude, searched_keyword, nearest_city)
    mycursor.execute(sql, val)
    mydb.commit()

def addWord(mydb, mycursor,word):
    """
    Adds a word in the database
    ----------
    Parameters :
        - mydb (mysql.connector.connection.MySQLConnection) : the database connection
        - mycursor (mysql.connector.cursor.MySQLCursor) : a cursor of the connection
        - word (str) : a word
    """
    sql = "REPLACE INTO word (label) VALUES ('"+word+"')"
    mycursor.execute(sql)
    mydb.commit()

def addCity(mydb, mycursor,city):
    """
    Adds a city in the database
    ----------
    Parameters :
        - mydb (mysql.connector.connection.MySQLConnection) : the database connection
        - mycursor (mysql.connector.cursor.MySQLCursor) : a cursor of the connection
        - city (str) : a city
    """
    sql = "REPLACE INTO city (city_name) VALUES ('"+city+"')"
    mycursor.execute(sql)
    mydb.commit()

def addKeywords(mydb, mycursor,numero_tweet, city, wordList):
    """
    Adds a keyword in the database
    ----------
    Parameters :
        - mydb (mysql.connector.connection.MySQLConnection) : the database connection
        - mycursor (mysql.connector.cursor.MySQLCursor) : a cursor of the connection
        - numero_tweet (str) : a numero_tweet
        - city (str) : a city
        - wordList (str) : a word
    """
    addCity(mydb, mycursor,city)
    for word in wordList:
        addWord(mydb, mycursor,word)
        sql = "REPLACE INTO keyword (numero_tweet,city_name,label) VALUES (%s, %s, %s)"
        val = (numero_tweet, city, word)
        mycursor.execute(sql,val)
        mydb.commit()

def deleteQuestionMarksOnly(mydb, mycursor):
    """
    delete question marks from keyword and word
    ----------
    Parameters :
        - mydb (mysql.connector.connection.MySQLConnection) : the database connection
        - mycursor (mysql.connector.cursor.MySQLCursor) : a cursor of the connection
    """
    for i in range(100):
        str = ""
        for j in range(i):
            str += "?"
        sql = "DELETE FROM keyword WHERE label LIKE '"+str+"';"
        mycursor.execute(sql)
        sql = "DELETE FROM word WHERE label LIKE '"+str+"';"
        mycursor.execute(sql)
        mydb.commit()

def mostUsedKeywords(mycursor,ville,nbmax):
    """
    Select the first "nbmax" most used keywords
    ----------
    Parameters :
        - mycursor (mysql.connector.cursor.MySQLCursor) : a cursor of the connection
        - ville (str) : a city
        - nbmax (str) : the number of the most used keyword we want
    """
    mycursor.execute("SELECT label, city_name,count(*) FROM keyword WHERE city_name like '"+ville+"' GROUP BY city_name,label ORDER BY `count(*)` DESC")
    myresult = mycursor.fetchall()
    if(myresult):
        print("Liste des",nbmax,"mots-clés (keywords) les plus utilisés dans les tweets de la ville de",ville,":")
        for i,line in enumerate(myresult):
            if(i<nbmax):
                print("-",line[0],"("+str(line[2])+")")
    else:
        print("Aucun mot-clé n'a été enregistré dans la ville de",ville+".")
