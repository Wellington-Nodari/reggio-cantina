from flask import Flask, render_template, redirect, url_for, session, flash, g
from functools import wraps
import os
import psycopg2

app = Flask(__name__)
#DATABASE_URL = os.environ['DATABASE_URL']

#conn = psycopg2.connect(database = "decidsulj18q74", user = "fphmyvegucmiih", password = "08bdb827e02af0eae42038539b24ecbb0bede1a077e2b210c57c326d77b5aa61", host = "ec2-3-248-121-12.eu-west-1.compute.amazonaws.com", port = "5432")
#conn = psycopg2.connect(DATABASE_URL, sslmode='require')

@app.route('/')
def home():
    return render_template("/home.html")

@app.route('/restaurant')
def restaurant():
    return render_template("/restaurant.html")

@app.route('/menu')
def menu():
    return render_template("/menu.html")

@app.route('/reservation')
def reservation():
    return render_template("/reservation.html")

@app.route('/findus')
def findus():
    return render_template("/findus.html")

@app.route('/admin')
def admin():
    return render_template("/adm_page.html")

@app.route('/login')
def login():
    return render_template("/login.html")

@app.route('/signup')
def signup():
    return render_template("/signup.html")

# @app.route('/admin', methods=['GET', 'POST'])
# @login_required
# def admin():
#     user_email = session['email']
#     if session is None:
#         error = 'Access denied. Login required!'
#         return render_template("/html/index.html", error=error)
#     else:
#         return render_template("/adm_page.html")

if __name__ == '__main__':
    app.run(debug=True)