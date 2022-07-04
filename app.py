from flask import Flask, render_template, redirect, url_for, session, flash, g
from calendary import Calendary
from datetime import datetime

app = Flask(__name__)

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
    cal = Calendary(2022)
    month = cal.month(6)
    return render_template("/reservation.html", cal=month)

@app.route('/findus')
def findus():
    return render_template("/findus.html")

@app.route('/admin')
def admin():
    return render_template("/adm_page.html")

@app.route('/signup')
def signup():
    return render_template("/signup.html")

if __name__ == '__main__':
    app.run(debug=True)