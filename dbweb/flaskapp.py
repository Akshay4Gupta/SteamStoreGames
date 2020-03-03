
import psycopg2
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import Required, Email

app = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    message = ''
    data = [] 
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password') 

        if username == None or password == None:
            return render_template('index.html', message=message)
        
        else:
            conn, cursor = db()
            check_if_present = "select case when (select count(*) from ((select 1 from users where uname = %s and pwd = %s)) as a) = 0 then 0 else (select count(*) from ((select 1 from users where uname = %s and pwd = %s)) as a) end;"
            message = 'You are Logged in.'
            cursor.execute(check_if_present % ("\'%s\'"%username,"\'%s\'"%password, "\'%s\'"%username,"\'%s\'"%password))
            data = cursor.fetchall()
            print(data)

            if data[0] == (0,): 
                message = 'Such user doesnt exists.'
                return render_template('index.html', message=message)
            
            elif data[0] == (1,):
                message = 'You are Logged in.'
                return redirect(url_for('display'))



    else:
        return render_template('index.html', message=message)

@app.route('/acc_display', methods=['GET', 'POST'])
def display():
    return render_template('acc_display.html')



@app.route('/topsellpage', methods=['GET', 'POST'])
def filtergenres():
    return render_template('attemptfirst.html')


@app.route('/redirecttopsell', methods=['GET', 'POST'])
def retrievedata():
    if request.method == "POST":
        conn, cursor = db()
        details = request.get_json()["data"]
        # print(details)
        genrelist = []
        nplist = []
        searchfind = ""
        # dictdata = {}

        if 'np' in details:
            npfind = details['np']
            nplist = npfind.split(",") 
        
        if 'gt' in details:
            genrefind = details['gt']
            genrelist = genrefind.split(",")

        if 'searching' in details:
            print(details)
            searchfind = details['searching']
            print(searchfind)

        # print(nplist)
        
        if searchfind == "":

            if nplist == []:
                genrefindquery = "select name, genres, price, appid from asteam where Array%s <@ genres;"
                cursor.execute(genrefindquery%genrelist)
                tab = cursor.fetchall()

            elif genrelist == []:
                npfindquery = "select name, genres, price, appid from asteam where Array%s <@ categories;"
                cursor.execute(npfindquery%nplist)
                tab = cursor.fetchall()

            else :
                andquery = "(select name, genres, price, appid from asteam where Array%s <@ categories) intersect (select name, genres, price, appid from asteam where Array%s <@ genres)"
                cursor.execute(andquery%(nplist, genrelist))
                tab = cursor.fetchall()


        else:

            if nplist == [] and genrelist == []:
                # searchquery = "select * from %s;"
                # cursor.execute(searchquery%(games(searchfind))
                cursor.execute("SELECT * FROM games(%s::text)", (searchfind,))
                # cursor.callproc('games',"counter")
                tab = cursor.fetchall()

            else:
                if nplist == []:
                    genrefindquery = "(select name, genres, price, appid from asteam where Array%s <@ genres) intersect (SELECT * FROM games(%s::text)))"%searchfind
                    cursor.execute(genrefindquery%(genrelist,searchfind))
                    tab = cursor.fetchall()

                elif genrelist == []:
                    npfindquery = "(select name, genres, price, appid from asteam where Array%s <@ categories) intersect (SELECT * FROM games(%s::text)))"%searchfind
                    cursor.execute(npfindquery%(nplist,searchfind))
                    tab = cursor.fetchall()

                else :
                    andquery = "(select name, genres, price, appid  from asteam where Array%s <@ categories) intersect (select name, genres, price, appid from asteam where Array%s <@ genres) intersect (SELECT * FROM games(%s::text)))"%searchfind
                    cursor.execute(andquery%(nplist, genrelist, searchfind))
                    tab = cursor.fetchall()        


        print(tab)     
        cursor.close()
        conn.commit()
        return {"data": tab}
        # print("pahuch gya")
        # return render_template('attemptfirst.html', dictdata = {"data": tab})
    else:
        conn, cursor = db()
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
        # print(tab)     
        # resp = jsonify(tab)
        # print(resp)
        cursor.close()
        conn.commit()

        return render_template('attemptfirst.html')


def db():
    try:

        conn = psycopg2.connect(host = "0.0.0.0", database = "project1", user = "postgres", password = "121996")

        cursor = conn.cursor()
        return conn, cursor

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)



if __name__ == '__main__':
    app.run(debug=True)



