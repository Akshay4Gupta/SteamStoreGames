from flask import Flask, url_for, redirect, render_template, request, Response, session, redirect
import psycopg2
import json
import getpass

app = Flask(__name__)
app.secret_key = 'NGPTO'

try:
    connection = psycopg2.connect(host='10.17.50.126', database="group_3", user = "group_3", password='202-901-602')
    cursor = connection.cursor()

    def delete_filter_data():
        if 'genres' in session:
            session.pop('genres', None)
        if 'categories' in session:
            session.pop('categories', None)

    @app.route('/')
    def load():

        delete_filter_data()
        # keys = list(session.keys())
        # for key in keys:
        #     if key != 'user' and key != 'current_url':
        #         session.pop(key, None)

        # print(len(session))

        print("Function1")
        loginval = 'Login'
        user = 'Welcome'
        if 'user' in session:
            loginval = 'Logout'
            user = session['user']

        return render_template('front_page.html', login = loginval, user = user)


    @app.route('/acc_display', methods=['GET', 'POST'])
    def display():
        delete_filter_data()
         # keys = list(session.keys())
         # for key in keys:
         #     if key != 'user' and key != 'current_url':
         #         session.pop(key, None)
        print("Function2")
        return render_template('acc_display.html')


    @app.route('/topsellpage', methods=['GET', 'POST'])
    def filtergenres():
         # keys = list(session.keys())
         # for key in keys:
         #     if key != 'user' and key != 'current_url':
         #         session.pop(key, None)
        print("Function3")
        return render_template('attemptfirst.html')

    @app.route('/filter')
    def filtergames():
        delete_filter_data()
         # keys = list(session.keys())
         # for key in keys:
         #     if key != 'user' and key != 'current_url':
         #         session.pop(key, None)
        print("Function4")
        loginval = 'Login'
        user = 'Welcome'

        if 'user' in session:
            loginval = 'Logout'
            user = session['user']
            print(session['user'])

        query = 'SELECT appid, name, release_date, header_image, genres, achievements, positive_ratings, negative_ratings, average_playtime, developer, price FROM asteam, mediadata WHERE steam_appid = appid '
        games = []
        req_args = request.args.copy()

        filters = ['genres', 'categories']

        for filter in filters:
            if filter in req_args:
                # print("Genres:", req_args['genres'])
                filterstring = req_args[filter].replace('"', "'")
                print(filterstring)
                req_args[filter] = req_args[filter].replace('"','')
                req_args[filter] = req_args[filter][1:len(req_args[filter])-1].split(",")
                # print("New Genres: ", req_args['genres'])
                session[filter] = req_args[filter]
                query += "AND ARRAY{} <@ {} ".format(filterstring, filter)

        if req_args["filterValue"] == 'Topsellers':
            # select appid, name, release_date, header_image, genres, achievements, positive_ratings, negative_ratings, average_playtime, developer, price from asteam, mediadata where steam_appid = appid limit 50;
            query += "ORDER BY CAST(SPLIT_PART(owners, '-', 2) AS INTEGER) DESC, (positive_ratings - negative_ratings) DESC LIMIT 20;"
        elif req_args["filterValue"] == 'Newreleases':
            query += "AND NOT(ARRAY['Early Access'] <@ steamspy_tags) ORDER BY release_date DESC LIMIT 20;"
        elif req_args["filterValue"] == 'Upcoming':
            query += "AND ARRAY['Early Access'] <@ steamspy_tags ORDER BY release_date DESC LIMIT 20;"
        elif req_args["filterValue"] == 'VR':
            query_inter = "WITH relids AS ((SELECT steam_appid as relid FROM descriptiondata WHERE UPPER(detailed_description) LIKE '% VR%' OR LOWER(detailed_description) LIKE '%virtual reality%') UNION (SELECT appid FROM asteam WHERE 'VR' = ANY(steamspy_tags) OR 'VR Only' = ANY(steamspy_tags))) "
            query = query.replace("asteam,", "asteam, relids,")
            query += "AND appid = relid ORDER BY (positive_ratings-negative_ratings) DESC LIMIT 20;"
            query = query_inter + query
        elif req_args["filterValue"] == 'Steamcontroller':
            query_inter = "WITH relids AS (SELECT steam_appid AS relid FROM requirementsdata WHERE linux_requirements LIKE '%steam%' OR pc_requirements LIKE '%steam%' OR mac_requirements LIKE '%steam%') "
            query = query.replace("asteam,", "asteam, relids,")
            query += "AND appid = relid ORDER BY (positive_ratings-negative_ratings) DESC LIMIT 20;"
            query = query_inter + query
        elif req_args["filterValue"] == 'Recfriends':
            if 'user' in session:
                pass
                # query = "select distinct cart.appid from (select * from personalappid('{}')) personalappid, cart where userid2 = userid and cart.appid <> personalappid.appid and boughtornot  = true except select distinct appid from personalappid;".format(session['user'])
            else:
                pass
        else:
            query += ";"

        session['query'] = query
        # print(games)
        return redirect("/" + req_args["filterValue"])

    @app.route('/redirecttopsell', methods=['GET', 'POST'])
    def retrievedata():
        # conn, cursor = db()
        details = []
        pricedetails = []
        print("detaillllllls %s"%request.get_json())
        if request.method == "POST":
            if 'data' in request.get_json():
                details = request.get_json()["data"]
            

            if 'pricedata' in request.get_json():

                pricedetails = request.get_json()["pricedata"]
            # print(details)
            genrelist = []
            nplist = []
            searchfind = ""
            lowerlim = 0
            upperlim = 500

            # dictdata = {}

            if 'np' in details:
                npfind = details['np']
                if npfind == '':
                    nplist = []
                else:
                    nplist = npfind.split(",") 
            
            if 'gt' in details:
                genrefind = details['gt']
                
                if genrefind == '':
                    genrelist = []
                else :
                    genrelist = genrefind.split(",")

            if 'searching' in details:
                print(details)
                searchfind = details['searching']
                print(searchfind)
            
            if 'minprice' in pricedetails:
                lowerlim = float(pricedetails["minprice"])

            if 'maxprice' in pricedetails:
                upperlim = float(pricedetails["maxprice"])

            # print(nplist)
            print(lowerlim)
            print(upperlim)
            print("nplist %s"%nplist)
            print("genrelist %s"%genrelist)
            if searchfind == "":

                if nplist == []:
                    genrefindquery = "select name, genres, price, appid, header_image from asteam, mediadata where (Array%s::text[] <@ genres) and (price between %s and %s) and steam_appid = appid;"
                    cursor.execute(genrefindquery%(genrelist, lowerlim, upperlim))
                    tab = cursor.fetchall()

                elif genrelist == []:
                    npfindquery = "select name, genres, price, appid from asteam where Array%s <@ categories and price between %s and %s;"
                    cursor.execute(npfindquery%(nplist, lowerlim, upperlim))
                    tab = cursor.fetchall()

                else :
                    andquery = "(select name, genres, price, appid from asteam where Array%s <@ categories and price between %s and %s) intersect (select name, genres, price, appid from asteam where Array%s <@ genres)"
                    cursor.execute(andquery%(nplist, lowerlim, upperlim, genrelist))
                    tab = cursor.fetchall()


            else:

                if nplist == [] and genrelist == []:

                    cursor.execute("SELECT * FROM games(%s::text) where cost between %s and %s", (searchfind,lowerlim,upperlim))
                    tab = cursor.fetchall()

                else:
                    if nplist == []:
                        genrefindquery = "(select name, genres, price, appid from asteam where Array%s <@ genres and price between %s and %s) intersect (SELECT * FROM games(%s::text)))"%searchfind
                        cursor.execute(genrefindquery%(genrelist, lowerlim, upperlim, searchfind))
                        tab = cursor.fetchall()

                    elif genrelist == []:
                        npfindquery = "(select name, genres, price, appid from asteam where Array%s <@ categories and price between %s and %s) intersect (SELECT * FROM games(%s::text)))"%searchfind
                        cursor.execute(npfindquery%(nplist, lowerlim, upperlim, searchfind))
                        tab = cursor.fetchall()

                    else :
                        andquery = "(select name, genres, price, appid  from asteam where Array%s <@ categories and price between %s and %s) intersect (select name, genres, price, appid from asteam where Array%s <@ genres) intersect (SELECT * FROM games(%s::text)))"
                        cursor.execute(andquery%(nplist,lowerlim, upperlim, genrelist, searchfind))
                        tab = cursor.fetchall()        


            # appidtuple = ()
            # for tup in tab:
            #     appidtuple.append(tup[3])

            # gamequery = "select steam_appid, header_image from mediadata where steam_appid in appidtuple;"
            # cursor.execute(gamequery)
            # tab2 = cursor.fetchall()

            print(tab)
            
            return {"data": tab}
        else:
            details =  request.args
            # print(details)
            genrefind = details['gt[]']
            # print(genrefind)
            genrelist1 = genrefind.split(",")
            # genrelist = []
            # for i in genrefind:
            #     if i != '':
            #         genrelist.append(i)
            # print(genrelist)
            genrelist = genrelist1[:-1]
            genrefindquery = "select name, genres from asteam where Array%s <@ genres;"
            cursor.execute(genrefindquery%genrelist)
            tab = cursor.fetchall()
            return render_template('attemptfirst.html')
        # cursor.close()
        # conn.commit()


    @app.route('/recommended/')
    def recommended():
        delete_filter_data()
         # keys = list(session.keys())
         # for key in keys:
         #     if key != 'user' and key != 'current_url':
         #         session.pop(key, None)
        print("Function6")
        loginval = 'Login'
        user = 'Welcome'
        if 'user' in session:
            loginval = 'Logout'
            user = session['user']
            print(session['user'])
        else:
            print('Poor thing :)')

        query = 'select appid, name, release_date, header_image, genres, achievements, positive_ratings, negative_ratings, average_playtime, developer, price from asteam, mediadata where steam_appid = appid limit 50;'
        cursor.execute(query)
        result = cursor.fetchall()
        loggedin = ''

        return render_template('recommended.html', login = loginval, user = user, recommendations = result)


    @app.route('/alag/<drona>')
    def game(drona):
        delete_filter_data()
         # keys = list(session.keys())
         # for key in keys:
         #     if key != 'user' and key != 'current_url':
         #         session.pop(key, None)
        print("Function7")
        loginval = 'Login'
        user = 'Welcome'
        if 'user' in session:
            loginval = 'Logout'
            user = session['user']
            print(session['user'])
        else:
            print('Poor thing :)')
        if drona.isdigit():
            query = 'select * from descriptiondata where steam_appid = '+drona+';'
            cursor.execute(query)
            result = cursor.fetchone()
            # resultnext = cursor.fetchall() #for the next page result
            cursor.execute('select * from asteam where appid = ' + drona + ';')
            result2 = cursor.fetchone()
            cursor.execute('select * from mediadata where steam_appid = ' + drona + ';')
            mediadata = cursor.fetchone()
            if (not (mediadata[2] == None) and (mediadata[2].startswith("{") or mediadata[2].startswith("["))) and ((not (mediadata[4] == None)) and (mediadata[4].startswith("{") or mediadata[4].startswith("["))):
                mediadata = mediadata[0], mediadata[1], eval(mediadata[2]), mediadata[3], eval(mediadata[4])
            elif((not (mediadata[2] == None)) and (mediadata[2].startswith("{") or mediadata[2].startswith("["))):
                mediadata = mediadata[0], mediadata[1], eval(mediadata[2]), mediadata[3], (mediadata[4])
            elif((not (mediadata[2] == None)) and (mediadata[4].startswith("{") or mediadata[4].startswith("["))):
                mediadata = mediadata[0], mediadata[1], (mediadata[2]), mediadata[3], eval(mediadata[4])
            else:
                mediadata = mediadata[0], mediadata[1], (mediadata[2]), mediadata[3], (mediadata[4])
            cursor.execute('select * from requirementsdatanew where steam_appid = ' + drona + ';')
            requirementsdata = cursor.fetchone()

            incartornot = 0
            positive_color = 'white'
            negative_color = 'white'

            if 'user' in session:
                cursor.execute("SELECT * FROM cart WHERE appid = {} AND userid = '{}'".format(drona, session['user']))
                incartornot = cursor.rowcount

                cursor.execute("SELECT vote FROM vote WHERE appid = {} AND userid = '{}'".format(drona, session['user']))

                row = cursor.fetchone()

                if row is not None:
                    if row[0] == True:
                        positive_color = 'green'
                    else:
                        negative_color = 'red'

            connection.commit()
            return render_template('mine.html', login = loginval, user = user, gameRequirements = requirementsdata, gameMedia = mediadata, gameMinuteDetails = result2, description = result[1][2:-2], aboutGame = result[2], shortDescription = result[3], incartornot = incartornot, pcolor = positive_color, ncolor = negative_color)
        else:
            return redirect('/alag/10')

    @app.route('/<name>')
    def b(name):
        delete_filter_data()
         # keys = list(session.keys())
         # for key in keys:
         #     if key != 'user' and key != 'current_url':
         #         session.pop(key, None)
        print("Function8")
        loginval = 'Login'
        user = 'Welcome'
        if 'user' in session:
            loginval = 'Logout'
            user = session['user']
            print(session['user'])
        else:
            print('Poor thing :)')

        if name == 'bhokali':
            name = {'phy':50,'che':60,'maths':70}
        return render_template('index.html', login=loginval, user=user, name = name)

    @app.route('/admin/')
    def hello_admin():
        delete_filter_data()
         # keys = list(session.keys())
         # for key in keys:
         #     if key != 'user' and key != 'current_url':
         #         session.pop(key, None)
        print("Function9")
        return "hello admin"

    @app.route('/guest/<guest>/')
    def hello_guest(guest):
        delete_filter_data()
         # keys = list(session.keys())
         # for key in keys:
         #     if key != 'user' and key != 'current_url':
         #         session.pop(key, None)
        print("Function10")
        return "hello %s" % guest

    @app.route('/user/<name>/')
    def hello_world(name):
        delete_filter_data()
         # keys = list(session.keys())
         # for key in keys:
         #     if key != 'user' and key != 'current_url':
         #         session.pop(key, None)
        print("Function11")
        if name == 'admin':
            return redirect(url_for('hello_admin'))
        else:
            return redirect(url_for('hello_guest', guest = name))

    @app.route('/vote', methods=['POST'])
    def vote():
        delete_filter_data()
         # keys = list(session.keys())
         # for key in keys:
         #     if key != 'user' and key != 'current_url':
         #         session.pop(key, None)
        print("Function12")
        req_args = request.form
        polarity = req_args['polarity']
        appid = req_args['appid']
        query = "SELECT * FROM vote WHERE userid = '{}' AND appid = {}".format(session['user'], appid, polarity)
        cursor.execute(query)
        if cursor.rowcount > 0:
            query = "UPDATE vote SET vote = {} WHERE userid = '{}' AND appid = {}".format(polarity, session['user'], appid)
        else:
            query = "INSERT INTO vote VALUES ('{}', {}, {})".format(session['user'], appid, polarity)

        cursor.execute(query)
        return "SUCCESS"
        # connection.commit()

    # @app.route('/login', methods = ['POST', 'GET'])
    # def bhokali():
    #     if request.method == 'POST':
    #         user = request.form['nm']
    #         return redirect(url_for('hello_world', name = user))
    #     else:
    #         user = request.args.get('nm')
    #         return redirect(url_for('hello_guest', guest = user))

    @app.route('/loginload')
    def login_users():
        delete_filter_data()
         # keys = list(session.keys())
         # for key in keys:
         #     if key != 'user' and key != 'current_url':
         #         session.pop(key, None)
        print("Function13")
        loginval = 'Login'
        user = 'Welcome'
        if 'user' in session:
            loginval = 'Logout'
            user = session['user']
            print(session['user'])
        else:
            print('WT thing :)')

        current_url = ''

        if 'current_url' in session:
            print(session['current_url'])
            current_url = session['current_url']
        else:
            current_url = "/login_load"

        return render_template("login.html", login=loginval, user=user, currurl=current_url)

    @app.route('/login', methods=['GET', 'POST'])
    def save_url():
        delete_filter_data()
        # print(request.method)
         # keys = list(session.keys())
         # for key in keys:
         #     if key != 'user' and key != 'current_url':
         #         session.pop(key, None)
        print("Function14")
        if request.method == 'GET':
            # print(url_for('login_users'))
            if 'current_url' not in session:
                session['current_url'] = "/"

            return redirect('/loginload')
        else:
            # print('Hello! :)')
            session['current_url'] = request.form["current_url"]
            return("Current url set!")

    @app.route('/login_user', methods=['POST'])
    def check_login_validity():
        delete_filter_data()
         # keys = list(session.keys())
         # for key in keys:
         #     if key != 'user' and key != 'current_url':
         #         session.pop(key, None)
        session.pop('current_url', None)
        print("Function15")
        req_args = request.form
        check_validity = "SELECT * FROM userdetails WHERE userid = '{}' AND pass = '{}';".format(req_args['user'], req_args['pass'])
        cursor.execute(check_validity)
        userfound = cursor.rowcount
        print(userfound)
        if(userfound == 0):
            print("Nooooooooooooooooooooooooooooooooooooooo")
            return 'NOT_FOUND'
        else:
            session['user'] = req_args['user']
            loginval = 'Logout'
            print("Yesssssssssssssssssssssssssssssssssssss")
            return 'FOUND'

        return render_template('recommended.html')

    @app.route('/logout_user', methods=['GET'])
    def logout_user():
        delete_filter_data()
         # keys = list(session.keys())
         # for key in keys:
         #     if key != 'user' and key != 'current_url':
         #         session.pop(key, None)
        print("Function16")
        loginval = 'Login'
        session.pop('user', None)
        return "Logged OUT!"

    @app.route('/login_fail')
    def show_failure():
        delete_filter_data()
        print("Function17")
         # keys = list(session.keys())
         # for key in keys:
         #     if key != 'user' and key != 'current_url':
         #         session.pop(key, None)
        loginval = 'Login'
        user = 'Welcome'
        if 'user' in session:
            loginval = 'Logout'
            user = session['user']
            print(session['user'])
        else:
            print('Poor thing :)')
        return render_template("loginfail.html", login=loginval, user=user)


    @app.route('/cart', methods = ['GET'])
    def render_cart():
        delete_filter_data()
        print("Function18")
         # keys = list(session.keys())
         # for key in keys:
         #     if key != 'user' and key != 'current_url':
         #         session.pop(key, None)
        loginval = 'Login'
        user = 'Welcome'
        if 'user' in session:
            loginval = 'Logout'
            user = session['user']
            print(session['user'])
        else:
            print('Poor thing :)')

        if 'user' in session:
            query = "SELECT asteam.appid, name, price FROM asteam, cart WHERE asteam.appid = cart.appid AND userid = '{}' AND incartornot = true;".format(session['user'])
            cursor.execute(query)
            tableA = cursor.fetchall()
            query = "SELECT asteam.appid, name FROM asteam, cart WHERE asteam.appid = cart.appid AND userid = '{}' AND boughtornot = true;".format(session['user'])
            cursor.execute(query)
            tableB = cursor.fetchall()
            print(tableA)
            print(tableB)
            return render_template("cart.html", table1 = tableA, table2 = tableB, login=loginval)

        else:
            return("Thou has't failed at logging in :)")

    @app.route('/addtocart', methods = ['POST'])
    def add_to_cart():
        delete_filter_data()
        print("Function19")
         # keys = list(session.keys())
         # for key in keys:
         #     if key != 'user' and key != 'current_url':
         #         session.pop(key, None)
        loginval = 'Login'
        user = 'Welcome'
        if 'user' in session:
            loginval = 'Logout'
            user = session['user']
            print(session['user'])
        else:
            print('Poor thing :)')

        req_args = request.form
        game_id = req_args["game_id"]
        # print(game_id)
        if 'user' in session:
            select_query = "INSERT INTO cart VALUES ('{}', {}, true)".format(session['user'], game_id)
            cursor.execute(select_query)
            # connection.commit()
            return "SUCCESS!"
        else:
            return "FAILURE!"
    # app.add_url_rule('/', 'ehlo', hello_world)

    @app.route('/bought', methods = ['POST'])
    def bought():
        delete_filter_data()
        print("Function20")
         # keys = list(session.keys())
         # for key in keys:
         #     if key != 'user' and key != 'current_url':
         #         session.pop(key, None)

        loginval = 'Login'
        user = 'Welcome'
        if 'user' in session:
            loginval = 'Logout'
            user = session['user']
            print(session['user'])
        else:
            print('Poor thing :)')

        req_args = request.form
        game_id = req_args["game_id"]
        query = "UPDATE cart SET incartornot = false, boughtornot = true WHERE appid = {};".format(game_id)
        cursor.execute(query)
        # connection.commit()

        return "SUCCESS!"

    # @app.route('/checkboxes')
    # def checkbox():
    #     return render_template("attemptfirst.html")

    @app.route('/Topsellers')
    def top():
        return loadtemp()

    @app.route('/Newreleases')
    def new():
        return loadtemp()

    @app.route('/Upcoming')
    def up():
        return loadtemp()

    @app.route('/VR')
    def vr():
        return loadtemp()

    def loadtemp():
        loginval = 'Login'
        user = 'Welcome'

        if 'user' in session:
            loginval = 'Logout'
            print(session['user'])
        else:
            print('Poor thing :)')

        query = session['query']

        dict = {"Indie":'', "Action":'', "Adventure":'', "Casual":'', "RPG":''}
        dict2 = {"Single-player":'', "Multi-player":'', "Co-op":'', "Full controller support":'', "Online Multi-Player":'', "Online Co-op":''}

        if 'genres' in session:
            for key in session['genres']:
                dict[key] = 'checked'

        if 'categories' in session:
            for key in session['categories']:
                dict2[key] = 'checked'

        cursor.execute(query)
        game = cursor.fetchall()


        return render_template("recommended.html", login = loginval, user = user, recommendations = game, genredict = dict, categorydict = dict2)

    @app.route('/test')
    def test():
        return "test func"


# def db():
#     try:
#         conn = psycopg2.connect(database="group_3", user = "group_3", password='202-901-602', host = "10.17.50.126")
#         cursor = conn.cursor()
#         return conn, cursor

#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)



# except (Exception, psycopg2.Error) as error :
#     print ("Error while connecting to PostgreSQL", error)

except psycopg2.InterfaceError as exc:
    print(exc.message)
    connection = psycopg2.connect(database="group_3", user = "group_3", password='202-901-602', host = "10.17.50.126")
    cursor = connection.cursor()

finally:
    # if(connection):
    #     cursor.close()
    #     connection.close()

    print("PostgreSQL connection is closed")

if __name__ == '__main__':
    print(test())
    app.run(debug=True)