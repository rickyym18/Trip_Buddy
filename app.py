
from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import psycopg2    

app = Flask(__name__)

app.secret_key = 'hello'
# Connect to your postgres DB
conn = psycopg2.connect(dsn="postgres://jwccrizi:Nqfg52g2IyR2eJjsjTLLt7zldV3BZHpG@heffalump.db.elephantsql.com/jwccrizi")

# Open a cursor to perform database operations
cur = conn.cursor()

@app.route("/")
def login_reg():
    return render_template("login_reg.html")

@app.route("/home", methods=['GET'])
def root():
    cur.execute("SELECT * FROM trips;")
    results = cur.fetchall()
    return render_template("home.html", trips=results)


@app.route("/users", methods=['GET','POST'])
def users():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")    
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")

        cur.execute(f"INSERT INTO users(username, password, first_name, last_name) VALUES('{username}','{password}','{first_name}','{last_name}')")
        conn.commit()

        return redirect(url_for("login_reg"))
    
    if request.method == 'GET':
        cur.execute("SELECT id, username FROM users;")
        results = cur.fetchall()
        p_string = ""
        for user in results:
            print(user)
            p_string = p_string + f"<p>{user[0]},{user[1]}</p>"

        return p_string

@app.route("/login", methods=['POST'])
def login():
    error = ""
    if 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        cur.execute(f"SELECT username, password FROM users WHERE username = '{username}' AND password = '{password}' ")
        user = cur.fetchone()
        if user:
            session['user'] = user[0]
            session['password'] = user[1]
            return redirect(url_for("root"))

    return redirect(url_for("login_reg"))

@app.route("/logout", methods=['POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login_reg'))

@app.route("/trips", methods=['GET', 'POST'])
def creating_trip():
    if request.method == 'POST':
        city = request.form.get("city")
        state = request.form.get("state")
        category = request.form.get("category")
        date = request.form.get("date")
        start_time = request.form.get("start_time")

        cur.execute(f"INSERT INTO trips(city, state, category, date, start_time) VALUES('{city}', '{state}', '{category}', '{date}', '{start_time}')")
        conn.commit()

        return redirect(url_for("root"))

    if request.method == 'GET':
        cur.execute("SELECT * trips")
        results = cur.fetchall()
        p_string = ""

        for trip in results:
            print(trip)
            p_string += f"<p>{trip[0]}</p>"

        return p_string


@app.route("/trip/delete/", methods=['POST'])
def delete_trip():
    id = request.form.get("id")
    cur.execute(f"DELETE FROM trips WHERE id = '{id}'")
    conn.commit()
    return redirect(url_for("root"))

@app.route("/trip/<int:id>/update", methods=['GET'])
def trip(id):
    session['id'] = id
    return render_template("edit_trip.html")

@app.route("/trip/update", methods=['POST'])
def update_trip():
    city = request.form.get("city")
    state = request.form.get("state")
    category= request.form.get("category")
    date= request.form.get("date")
    start_time = request.form.get("start_time")

    cur.execute(f"UPDATE trips SET city = '{city}', state = '{state}', category = '{category}', date= '{date}', start_time = '{start_time}' WHERE id={session.get('id')}")
    conn.commit()
    return redirect(url_for("root"))





                
