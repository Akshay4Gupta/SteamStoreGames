import psycopg2
import os
import sys
import getpass
import string
import csv
from random import *
path = "../../ProjectData/"
def playsGame(l):
    return choice(l)
try:
    connection = psycopg2.connect(database="dummy", user = "postgres", password=getpass.getpass(prompt='Enter your password:\t'), host = "127.0.0.1", port = "5432")
    cursor = connection.cursor()
    filename = 'million_half.txt'
    GameIdFileName = 'asteam.csv'
    cursor.execute('select userid from userDetails;')
    file = cursor.fetchall()
    GameIdFile = csv.reader(open(os.path.join(path, GameIdFileName), 'r'))
    GameId = list()
    for row in GameIdFile:
        for uid in row:
            GameId.append(uid)
            break
    GameId.remove('appid')
    i = 0
    users = list()
    for i in file:
        users.append(i[0])

    toinsert = set()

    for i in range(300):
        toinsert.add((playsGame(GameId), playsGame(users)))
    for i, j in toinsert:
        choi = playsGame([False,True])
        query4 = 'insert into cart values ($${}$$, $${}$$, {}, {});'.format(j, i, choi, not choi)
        cursor.execute(query4)

    # for user in file:

        # i+=1
        # genPass = generatePass()
        # cursor.execute('select * from descriptiondata where steam_appid = ' + '285500' + ";")
        # print("________________________")
        # query = 'insert into userDetails values ($${}$$, $${}$$);'.format(user.strip(), genPass)
        # query3 = 'insert into friends values($${}$$, $${}$$);'.format(playsGame(GameId), playsGame(GameId))
        # BOOL = playsGame([True, False])
        # print(query)

        # cursor.execute(query)
        # cursor.execute(query2)
        # cursor.execute(query3)
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    if(connection):
        connection.commit()
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
