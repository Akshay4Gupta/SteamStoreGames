import psycopg2
import os
import sys
import getpass
import string
import csv
from random import *
path = "../../ProjectData/"
try:
    connection = psycopg2.connect(database="project", user = "postgres", password=getpass.getpass(prompt='Enter your password:\t'), host = "127.0.0.1", port = "5432")
    cursor = connection.cursor()
    cursor.execute("select column_name from information_schema.columns where table_name = 'steamspytagdata'")
    query = "select "
    again = False
    colu = []
    for row in cursor.fetchall():
        for element in row:
            if again:
                query += ", "
            query += "sum({}) as {}".format(element, element)
            colu.append(element)
            again = True
            break
    query += " from steamspytagdata ;"
    cursor.execute(query)
    print(query)
    again = True
    for row in cursor.fetchall():
        for column, c in zip(row, colu):
            if again:
                again = False
                continue
            print(c, "\t\t\t", column)

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    if(connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
