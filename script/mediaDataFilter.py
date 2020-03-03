import psycopg2
import getpass
import csv
import os
import json
import sys
from pprint import pprint

path = "../../ProjectData/"
try:
    connection = psycopg2.connect(database="dummy", user = "postgres", password=getpass.getpass(prompt='Enter your password:\t'), host = "127.0.0.1", port = "5432")
    cursor = connection.cursor()
    GameIdFileName = 'mediadata'
    cursor.execute('select * from mediadata')
    result = cursor.fetchall()
    for i in result:
        steam_appid,header_image,screenshots,background,movies = i
        screenshots = getEverything(screenshots)
    '''    for row in GameIdFile:
        if row[0] == 'steam_appid':
            continue
        pc_requirements,mac_requirements,linux_requirements,minimum,recommended = row[1:]
        minreco =  minimum.split('Recommended:')
        if len(minreco) == 2:
            minimum, recommended = minreco
        # print("===============================================================")
        # print(pc_requirements)
        # print("--------------------------------")
        # print(mac_requirements)
        # print("--------------------------------")
        # print(linux_requirements)
        # print("--------------------------------")

        pc_requirements= pc_requirements.split('<strong>')
        (pc, mac, linux) = (getDict(pc_requirements), eval(mac_requirements), eval(linux_requirements))
        macModified = dict()
        for key in mac:
            if '<' in mac[key]:
                macModified = {key: (getDict(mac[key].split('<strong>')))}
            else:
                macModified = {key: (mac[key])}
        linuxModified = dict()
        if isinstance(linux, list):
            for i in linux:
                print(i)
                input()
        elif isinstance(linux, dict):
            for key in linux:
                if '<' in linux[key]:
                    linuxModified[key] = getDict(linux[key].split('<strong>'))
                else:
                    linuxModified[key] = (linux[key])
        else:
            print(type(linux))
            input()
        query = 'insert into requirementsdatanew values (%s, Json($$%s$$), Json($$%s$$), Json($$%s$$), $$%s$$, $$%s$$);' % (row[0], json.dumps(pc), json.dumps(macModified), json.dumps(linuxModified), minimum, recommended)
        try:
            cursor.execute(query)
        except Exception as error:
            print(query)
            connection.rollback()
            continue
    connection.commit()'''

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
