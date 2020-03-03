import psycopg2
import getpass
import csv
import os
import json
import sys
from pprint import pprint

def remove_html_tags(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def getDict(requirements):
    requirements_dict = dict()
    for i in requirements:
        dictEle = i.split('</strong>')
        if len(dictEle) == 2:
            requirements_dict[remove_html_tags(dictEle[0].replace('{', ''))] = remove_html_tags(dictEle[1].replace('}', '')).replace('\\r', '').replace('\\t', '').replace('\\n', '').replace("\\\\", ' / ').replace('\\xa0', '').replace('\\xad', '').replace("\\'", "'").replace("'", "''").replace('"', '\\"').strip()
    return requirements_dict

path = "../../ProjectData/"
try:
    connection = psycopg2.connect(database="dummy", user = "postgres", password=getpass.getpass(prompt='Enter your password:\t'), host = "127.0.0.1", port = "5432")
    cursor = connection.cursor()
    GameIdFileName = 'steam_requirements_data.csv'
    GameIdFile = csv.reader(open(os.path.join(path, GameIdFileName), 'r'))
    for row in GameIdFile:
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
    connection.commit()

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
