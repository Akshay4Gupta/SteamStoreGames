import psycopg2
from flask import Flask
from flask import request
from flask import Response
from flask import jsonify
from flask import render_template
from flask import redirect

app = Flask(__name__)

games = []

@app.route('/')
def display_results():
	conn, cursor = connect_to_db()
	create_game_table = "CREATE TABLE IF NOT EXISTS games(name TEXT, score FLOAT);"
	cursor.execute(create_game_table)
	insert = "INSERT INTO games VALUES ('Final Fantasy X', 9.3), ('Final Fantasy X', 9.5), ('Final Fantasy XIV', 8.5), ('Shadow of the Colossus', 9.7);"
	cursor.execute(insert)
	cursor.close()
	conn.commit()
	return render_template('test.html')

@app.route('/searchresults', methods = ['GET'])
def serve_get_request():

	req_args = request.args
	game = req_args['search']
	conn, cursor = connect_to_db()
	game_info = get_specific_games(cursor, game)

	# data = {}
	# data['game'] = []
	#
	# for game_tuple in game_info:
	# 	gi = []
	# 	for j in range(len(game_tuple)):
	# 		gi += [str(game_tuple[j])]
	# 	data['game'] += [gi]
	#
	# resp = jsonify(data)
	# resp.status_code = 200

	table_string = '<table><tr><th>Name</th><th>Score</th></tr>'

	for game in game_info:
		table_string += '<tr>'
		for column in game:
			table_string += '<td>' + str(column) + '</td>'
		table_string += '</tr>'

	table_string += '</table>'

	data = {}
	data['table_string'] = table_string

	resp = jsonify(data)
	resp.status_code = 200

	cursor.close()
	conn.commit()

	return resp

@app.route('/register', methods=['GET'])
def register_users():
	return render_template("register.html")
	# return redirect(url_for('display_results'))

@app.route('/register_user', methods=['POST'])
def register_users_in_the_database():
	req_args = request.form
	data = {}
	data['user'] = req_args['user']
	data['mail'] = req_args['mail']
	data['password'] = req_args['pass']
	resp = jsonify(data)
	resp.status_code = 200

	conn, cursor = connect_to_db()
	create_users_table = "CREATE TABLE IF NOT EXISTS users(name TEXT, email TEXT, password TEXT, games_purchased TEXT[], playtime INT, tags_used TEXT[], PRIMARY KEY(email));"
	cursor.execute(create_users_table)
	insert_current_user = "INSERT INTO users VALUES('{}', '{}', '{}', ARRAY[]::TEXT[], 	0, ARRAY[]::TEXT[]);".format(data['user'], data['mail'], data['password'])
	cursor.execute(insert_current_user)
	cursor.close()
	conn.commit()

	return resp

@app.route('/login', methods=['GET'])
def login_users():
	return render_template("login.html")

@app.route('/login_user', methods=['GET'])
def check_login_validity():
	req_args = request.form
	conn, cursor = connect_to_db()
	check_validity = "SELECT COUNT(*) FROM users WHERE email = {} AND password = {};".format(req_args['mail'], req_args['pass'])
	cursor.execute(check_validity)
	user = cursor.fetchall()

	if(user[0][0] == 0):
		return 'NOT_FOUND'
	else:
		return 'FOUND'

def connect_to_db():
	try:
		conn = psycopg2.connect(host = "0.0.0.0", database = "test_project", user = "postgres", password = "Pc9hj22V")
		cursor = conn.cursor()
		# create_game_table(cursor)
		# insert_values(cursor)
		# do_querying(cursor)
		# drop_table(cursor)
		#
		# cursor.close()
		# conn.commit()
		return conn, cursor

	except (Exception, psycopg2.DatabaseError) as error:
		print(error)


def create_game_table(cursor):
	query = 'CREATE TABLE games(name TEXT, score FLOAT);'
	cursor.execute(query)

def insert_values(cursor):
	query = "INSERT INTO games VALUES ('Final Fantasy X', 9.3), ('Final Fantasy XIV', 8.5), ('Shadow of the Colossus', 9.7);"
	cursor.execute(query)

def get_all_games(cursor):

	global games

	query = "SELECT * FROM games;"
	cursor.execute(query)

	print("The number of games is: ", cursor.rowcount)

	games = cursor.fetchall()
	print("The games are: ", games)

def get_specific_games(cursor, name):

	global games

	query = "SELECT * FROM games WHERE name LIKE '{}%';".format(name)
	cursor.execute(query)
	return cursor.fetchall()

def drop_table(cursor):
	query = "DROP TABLE games;"
	cursor.execute(query)

def stringify_results(results):

	string = ''

	for record in results:
		for value in record:
			string += str(value) + ' '
		string += '\n'

	return string

if __name__ == '__main__':
	app.run(debug=True)
