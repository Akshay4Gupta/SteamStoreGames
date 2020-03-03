import csv
import os
import psycopg2
import sys
import getpass
path = "../../ProjectData/"
try:
    connection = psycopg2.connect(database="dummy", user = "postgres", password=getpass.getpass(prompt='Enter your password:\t'), host = "127.0.0.1", port = "5432")
    cursor = connection.cursor()
except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
for filename in sorted(os.listdir(path)):
    if filename.endswith('fuckoff'):
        continue
    qcsvfile = open(os.path.join(path, filename), 'r')
    file = csv.reader(qcsvfile)
    tablename = filename.replace(".csv","")
    change = False

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
    change = True
    print(tablename)
    for rows in file:
        fuck = 0
        i = 0
        if change:
            change = False
            continue
        run = True
        if tablename != 'asteam':     # to check whether it is a foreign key or not
            try:
                for column in rows:
                    query = 'select * from asteam where appid = ' + column
                    cursor.execute(query)
                    if(cursor.rowcount == 0):
                        run = False
                    break
            except (Exception, psycopg2.Error) as error :
                print ("Error while connecting to PostgreSQL", error)
        if run:
            query = 'insert into ' + tablename + ' values ('
            next = False
            for column in rows:
                if tablename == 'descriptionData' and fuck >= 4:
                    continue
                fuck += 1
                if next:
                    query += ", "
                if ';' in column or (tablename == 'asteam' and i in [6, 8, 9, 10]):
                    column = (column.split(';'))
                    fudu = list()
                    for j in column:
                        if "'" in j:
                            fudu.append(j.replace("'", ""))
                        else:
                            fudu.append(j)
                    if len(fudu) == 0:
                        query += 'NULL'
                    else:
                        query += "array" + str(fudu)
                elif query.isdigit():
                    query += column
                else:
                    if column == '':
                        query += 'NULL'
                    else:
                        query += "E'" + column.replace('\\xa0', '').replace('\\xad', '').replace("\\'", "'").replace("'", "''").replace('"', '\\"') + "'"
                next = True
                i+=1
            query += ");"
            try:
                cursor.execute(query)
            except(Exception, psycopg2.Error) as error :
                print(query)
                print("Error while connecting to PostgreSQL", error)
                connection.rollback()
                continue
            try:
                connection.commit()
            except (Exception, psycopg2.Error) as error :
                print ("Error while connecting to PostgreSQL", error)
    qcsvfile.close()
if(connection):
    cursor.close()
    connection.close()
    print("PostgreSQL connection is closed")
