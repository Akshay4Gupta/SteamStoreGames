import csv
import os
import psycopg2
import sys
import getpass
# NGPTO
path = "../../ProjectData/"
intlist = ['steam_appid', 'appid', 'required_age', 'achievements']
floatlist = ['positive_ratings', 'negative_ratings', 'average_playtime', 'median_playtime', 'price']
textarray = ['platforms', 'categories', 'steamspy_tags', 'genres']
try:
    connection = psycopg2.connect(database="dummy", user = "postgres", password=getpass.getpass(prompt='Enter your password:\t'), host = "127.0.0.1", port = "5432")
    cursor = connection.cursor()
    for filename in sorted(os.listdir(path)):
        if filename.endswith('fuckoff'):
            continue
        file = csv.reader(open(os.path.join(path, filename), 'r'))
        qcsvfile = open(os.path.join(path, filename))
        tablename = filename.replace(".csv","")
        change = False
        if tablename != 'steam':
            tablename = tablename.replace("steam_", "")
            tableName = ''
            for l in tablename:
                if change:
                    tableName+=l.upper()
                    change = False
                elif l == "_":
                    change = True
                else:
                    tableName+=l
            tablename = tableName
        if len(sys.argv) >= 2:
            cursor.execute("drop table " + tablename + " cascade")
            connection.commit()
            continue
        change = True
        for rows in file:
            if change:
                query = "create table if not exists {} ({})"
                attribs = ''
                changeOfColumn = False
                for column in rows:
                    if not column.strip():
                        continue
                    if column in intlist or tablename == 'steamspyTagData':
                        type = 'int'
                    elif column in floatlist:
                        type = 'float'
                    elif column == 'owners':
                        type = 'text'
                    elif column in textarray:
                        type = 'text[]'
                    elif column == 'release_date':
                        type = 'date'
                    else:
                        type = 'text'
                    if changeOfColumn:
                        attribs += ", "
                    if column[0].isdigit() or column == 'foreign':
                        column = 'a' + column
                    if tablename == 'asteam' and column == 'appid':
                        attribs += column.replace('.', '').replace('&', '') + " " + type + " " + 'primary key'
                    elif column == 'steam_appid':
                        attribs += column.replace('.', '').replace('&', '') + " " + type + ' references asteam(appid)'
                    elif column == 'appid':
                        attribs += column.replace('.', '').replace('&', '') + " " + type + ' references asteam(appid)'
                    else:
                        attribs += column.replace('.', '').replace('&', '') + " " + type
                    changeOfColumn = True
                change = False
                cursor.execute(query.format(tablename, attribs))
                connection.commit()
            # else:
            #     cursor.copy_expert("copy {} from STDIN WITH CSV HEADER".format(tablename), qcsvfile)
            #     break
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
