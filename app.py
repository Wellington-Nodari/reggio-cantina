from flask import Flask, render_template, redirect, url_for, session, flash, request
from functools import wraps
import os
import psycopg2
import psycopg2.extras

app = Flask(__name__)
app.secret_key = "myfinalproject-DBSsoftwaredevelopment"

conn = psycopg2.connect(dbname = "decidsulj18q74", user = "fphmyvegucmiih", password = "08bdb827e02af0eae42038539b24ecbb0bede1a077e2b210c57c326d77b5aa61", host = "ec2-3-248-121-12.eu-west-1.compute.amazonaws.com")

def login_required(f): #taken from https://www.youtube.com/watch?v=_pzMDIi5BuI
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Please login first.')
            return redirect(url_for('home'))
    return wrap

@app.route('/')
def home():
    return render_template("/home.html")

@app.route('/restaurant')
def restaurant():
    return render_template("/restaurant.html")

@app.route('/menu')
def menu():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    m = '''SELECT * FROM menu WHERE item_category = 'meal' ORDER BY item_menu_id ASC;'''
    cur.execute(m)
    meal_list = cur.fetchall()

    d = '''SELECT * FROM menu WHERE item_category = 'dessert' ORDER BY item_menu_id ASC;'''
    cur.execute(d)
    dessert_list = cur.fetchall()

    w = '''SELECT * FROM menu WHERE item_category = 'drink' ORDER BY item_menu_id ASC;'''
    cur.execute(w)
    drink_list = cur.fetchall()

    return render_template("/menu.html", meal_list = meal_list, dessert_list = dessert_list, drink_list = drink_list)

@app.route('/reservation')
def reservation():
    return render_template("/reservation.html")

@app.route('/findus')
def findus():
    return render_template("/findus.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        email = str(request.form["email"])
        pwd = str(request.form["pwd"])
        cur.execute("SELECT email, pwd FROM login WHERE email='{}' AND pwd='{}';".format(email, pwd))
        row = cur.fetchall()
        try:
            if row[0][0] == email and row[0][1] == pwd:
                session['logged_in'] = True
                cur.close()
                session['email'] = email
                if session['logged_in'] is True:
                    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                    cur.execute("SELECT role_id FROM login WHERE email='{}'".format(email))
                    print('here')
                    role = cur.fetchall()
                    print(role[0][0])

                    if role[0][0] == 2:
                        cur.close()
                        return redirect(url_for('admin'))
                    elif role[0][0] == 3 and role[0][0] == 2:
                        cur.close()
                        return redirect(url_for('floor'))
                    elif role[0][0] == 4 and role[0][0] == 3 and role[0][0] == 2:
                        cur.close()
                        return redirect(url_for('kitchen'))
                    if role[0][0] == 1:
                        cur.close()
                        return redirect(url_for('menu'))
        except:
            error = 'Invalid credentials. Please try again'
            return render_template('/home.html', error=error)
    else:
        return render_template("/login.html")

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('home'))

@app.route('/signup', methods=['GET','POST'])
def signup():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        pwd = request.form['pwd']
        role_id = 1

        cur.execute("INSERT INTO customer(fname, lname, email, phone, address, role_id) VALUES(%s,%s,%s,%s,%s,%s)",(fname, lname, email, phone, address, role_id))

        cur.execute("INSERT INTO login(email, pwd, role_id) VALUES(%s,%s,%s)",(email, pwd, role_id))
        conn.commit()
        cur.close()
        flash('SignUp Successful')
        return redirect(url_for("home"))
    else:
        return render_template("/signup.html")

@app.route('/admin')
@login_required
def admin():
    email = str(session['email'])
    print(email)
    if session is None:
        print('session is none')
    else:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT role_id FROM staff WHERE email='{}'".format(email))
        role = cur.fetchall()

        cur.execute("SELECT fname FROM staff WHERE email='{}'".format(email))
        name = cur.fetchall()
        fname = name[0][0]

        if role[0][0] == 1:
            cur.close()
            return render_template("/adm_page.html", fname=fname)
        else:
            error = 'You do not have permission for accessing this page. Access denied!'
            return render_template("/home.html", error=error)

@app.route('/floor')
@login_required
def floor():
    email = str(session['email'])
    print(email)
    if session is None:
        print('session is none')
    else:
        return render_template("/floor.html")

@app.route('/kitchen')
@login_required
def kitchen():
    email = str(session['email'])
    print(email)
    if session is None:
        print('session is none')
    else:
        return render_template("/kitchen.html")

if __name__ == '__main__':
    app.run(debug=True)
