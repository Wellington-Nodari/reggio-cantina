from flask import Flask, render_template, redirect, url_for, session, flash, request
from functools import wraps
import psycopg2
import psycopg2.extras
import os

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

@app.route('/', methods=['GET', 'POST'])
def home():

    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        rating = request.form.get('note')
        review = request.form['review']
        print(name, email, rating, review)

        cur.execute("INSERT INTO review(rv_name, rv_email, rv_rating, review) VALUES(%s,%s,%s,%s)",
                    (name, email, rating, review))
        conn.commit()
        cur.close()
        flash('Review Submitted')

    try:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        r = '''SELECT rv_name, review, rv_rating FROM review ORDER BY rv_rating DESC;'''
        cur.execute(r)
        review_list = cur.fetchall()
    except:
        pass


    return render_template("/home.html", review_list=review_list)

@app.route('/restaurant')
def restaurant():
    return render_template("/restaurant.html")

@app.route('/menu', methods=['GET', 'POST'])
def menu():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    m = '''SELECT item_menu_id, item_name, item_desc FROM menu WHERE item_category = 'meal' ORDER BY item_menu_id ASC;'''
    cur.execute(m)
    meal_list = cur.fetchall()
    d = '''SELECT item_menu_id, item_name, item_desc FROM menu WHERE item_category = 'dessert' ORDER BY item_menu_id ASC;'''
    cur.execute(d)
    dessert_list = cur.fetchall()
    w = '''SELECT item_menu_id, item_name, item_desc FROM menu WHERE item_category = 'drink' ORDER BY item_menu_id ASC;'''
    cur.execute(w)
    drink_list = cur.fetchall()

    return render_template("/menu.html", meal_list=meal_list, dessert_list=dessert_list, drink_list=drink_list)

@app.route('/adm_menu', methods=['GET', 'POST'])
@login_required
def adm_menu():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    m = '''SELECT item_menu_id, item_name, item_desc, item_price FROM menu WHERE item_category = 'meal' ORDER BY item_menu_id ASC;'''
    cur.execute(m)
    meal_list = cur.fetchall()
    d = '''SELECT item_menu_id, item_name, item_desc, item_price FROM menu WHERE item_category = 'dessert' ORDER BY item_menu_id ASC;'''
    cur.execute(d)
    dessert_list = cur.fetchall()
    w = '''SELECT item_menu_id, item_name, item_desc, item_price FROM menu WHERE item_category = 'drink' ORDER BY item_menu_id ASC;'''
    cur.execute(w)
    drink_list = cur.fetchall()

    if session['logged_in'] is True:
        if request.method == 'POST':
            item_menu_id = request.form['item_menu_id']
            item_name = request.form['item_name']
            item_desc = request.form['item_desc']
            item_price = request.form['item_price']

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute('''
                    UPDATE menu
                    SET item_name = %s,
                        item_desc = %s,
                        item_price = %s
                    WHERE item_menu_id = %s;
                ''', (item_name, item_desc, item_price, item_menu_id))
            flash('Menu Updated Successfully')
            conn.commit()


            n_item_name = request.form['n_item_name']
            n_item_desc = request.form['n_item_desc']
            n_item_category = request.form['n_item_category']
            n_item_price = request.form['n_item_price']

            cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute("INSERT INTO menu(item_name, item_desc, item_category, item_price) VALUES(%s,%s,%s,%s);",(n_item_name, n_item_desc, n_item_category, n_item_price))
            flash('Menu Updated Successfully')
            conn.commit()

    return render_template("/adm_menu.html", meal_list = meal_list, dessert_list = dessert_list, drink_list = drink_list)

@app.route('/order', methods=['GET', 'POST'])
@login_required
def order():
    subtotal = 0.00
    email = str(session['email'])
    if session is None:
        print('session is none')

    else:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        cur.execute("SELECT fname FROM customer WHERE email='{}'".format(email))
        name = cur.fetchall()
        fname = name[0][0]

        m = '''SELECT item_menu_id, item_name, item_desc FROM menu WHERE item_category = 'meal' ORDER BY item_menu_id ASC;'''
        cur.execute(m)
        meal_list = cur.fetchall()
        d = '''SELECT item_menu_id, item_name, item_desc FROM menu WHERE item_category = 'dessert' ORDER BY item_menu_id ASC;'''
        cur.execute(d)
        dessert_list = cur.fetchall()
        w = '''SELECT item_menu_id, item_name, item_desc FROM menu WHERE item_category = 'drink' ORDER BY item_menu_id ASC;'''
        cur.execute(w)
        drink_list = cur.fetchall()

        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        m = '''SELECT item_name FROM menu ORDER BY item_menu_id ASC;'''
        cur.execute(m)
        order = cur.fetchall()

        if request.method == 'POST':
            varItm = ['item']
            varQty = ['quantity']
            for i in range(len(varItm)):
                while i <= 13:
                    varItm.append(f"item{i}")
                    varQty.append(f"quantity{i}")
                    i += 1
                    print(varItm[i])
                    try:
                        item = str(request.values[varItm[i]])
                        quantity = str(request.values[varQty[i]])
                        print(item)
                        # print(quantity)
                    except:
                        continue
                    if item is not None:
                        amount = 0
                        cur.execute("SELECT item_price FROM menu WHERE item_name='{}';".format(item))
                        price = cur.fetchall()
                        price_list = 0
                        for sublist in price:
                            for i in sublist:
                                price_list = float(i)
                        qty = float(quantity)
                        amount += (price_list * qty)
                        print(amount)

                        # cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                        # cur.execute("SELECT item_menu_id FROM menu WHERE item_name='{}';".format(item))
                        # idList = cur.fetchall()
                        # print(idList)
                        # id = 0
                        # for subIdlist in idList:
                        #     for item in subIdlist:
                        #         id = item
                        # d[id] = quantity
                    else:
                        break
                subtotal = (format(amount, '.2f'))


        return render_template("/cx-orders.html",fname=fname, meal_list = meal_list, dessert_list = dessert_list, drink_list = drink_list, items_list=order, subtotal=subtotal)

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
        cur.execute("SELECT * FROM login WHERE email='{}' AND pwd='{}';".format(email, pwd))
        row = cur.fetchall()
        print(row)

        if row[0][1] == email and row[0][2] == pwd:
            session['logged_in'] = True
            session['email'] = email
            if session['logged_in'] is True:
                cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
                cur.execute("SELECT role_id FROM login WHERE email='{}'".format(email))
                role = cur.fetchall()

                if role[0][0] == 2:
                    cur.close()
                    return redirect(url_for('admin'))

                if role[0][0] == 3:
                    cur.close()
                    return redirect(url_for('floor'))

                if role[0][0] == 4:
                    cur.close()
                    return redirect(url_for('kitchen'))

                if role[0][0] == 1:
                    cur.close()
                    return redirect(url_for('order'))

        else:
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
        pwdC = request.form['pwdC']
        role_id = 1

        cur.execute("SELECT email FROM customer")
        emailVal = cur.fetchall()
        email_list = []
        for sublist in emailVal:
            for item in sublist:
                email_list.append(item)

        if pwd != pwdC:
            return render_template('/signup.html', error='The passwords must match.')

        for i in email_list:
            if email not in email_list:
                pass
            else:
                return render_template('/signup.html', error='This email is in use. Please choose another one!')

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
    if session is None:
        print('session is none')
    else:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT role_id FROM staff WHERE email='{}'".format(email))
        role = cur.fetchall()

        cur.execute("SELECT fname FROM staff WHERE email='{}'".format(email))
        name = cur.fetchall()
        fname = name[0][0]

        if role[0][0] == 2:
            cur.close()
            return render_template("/adm_page.html", fname=fname)
        else:
            error = 'You do not have permission for accessing this page. Access denied!'
            return render_template("/home.html", error=error)

# @app.route('/staff')
# @login_required
# def staff():
#     email = str(session['email'])
#     return render_template("/staff.html")

@app.route('/floor')
@login_required
def floor():
    email = str(session['email'])
    if session is None:
        print('session is none')
    else:
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("SELECT role_id FROM staff WHERE email='{}'".format(email))
        role = cur.fetchall()
        print('flore')

        cur.execute("SELECT fname FROM staff WHERE email='{}'".format(email))
        name = cur.fetchall()
        fname = name[0][0]

        if role[0][0] == 3:
            cur.close()
            return render_template("/floor.html", fname=fname)
        else:
            error = 'You do not have permission for accessing this page. Access denied!'
            return render_template("/home.html", error=error)

@app.route('/kitchen')
@login_required
def kitchen():
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
        print(name)
        fname = name[0][0]

        if role[0][0] == 4:
            cur.close()
            return render_template("/kitchen.html", fname=fname)
        else:
            error = 'You do not have permission for accessing this page. Access denied!'
            return render_template("/home.html", error=error)

if __name__ == '__main__':
    app.run(debug=True)
