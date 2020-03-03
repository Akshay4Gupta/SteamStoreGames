# Steam-Store-Games
https://www.kaggle.com/nikdavis/steam-store-games#steam.csv

Before starting all this change the name of csv file steam.csv to asteam.csv


To create the table
-
python3 createTable.py

To drop all the tables
-
python3 createTable.py drop

To insert Data into the Table (please report if you get any errors in the commandline)
-
python3 filterACopyData.py

To insert the remaining data to sql table
-
open postgres and connect to project table
\i \path\to\insert.sql
