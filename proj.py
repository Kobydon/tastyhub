import sqlite3 
from flask import Flask ,flash,session,render_template,redirect,escape, url_for,request, send_from_directory
import sys
import cgi, os
import cgitb; cgitb.enable()
from werkzeug.utils import secure_filename

from flask_mail import Mail, Message
import time
from datetime import datetime
import collections
from psycopg2 import sql

from flask import g
import sqlite3
app = Flask(__name__)
app.secret_key = 'any random string'
# app.config['DATABASE'] = 'members.db'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'jxkalmhefacbuk@gmail.com'
app.config['MAIL_PASSWORD'] ='qhsf mguh pzuh dcmx'  # or use an app-specific password
app.config['MAIL_DEFAULT_SENDER'] = 'jxkalmhefacbuk@gmail.com'
app.config['UPLOAD_FOLDER_REST'] = 'static/restaurants/'
app.config['UPLOAD_FOLDER_DISH'] = 'static/dish/'

import psycopg2
mail = Mail(app)
# Gmail SMTP configuration





def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = psycopg2.connect(
            dbname='tastyh',
            user='tastyh_user',
            password='8YHmGY3f9YwCHXsC3AoIRbJNcO7m0NzA',
            host='dpg-cqohq7tsvqrc73fh9hhg-a.oregon-postgres.render.com',
            port='5432'  # Default PostgreSQL port, change if necessary
        )
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()

        # Create tables
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS approval (
                username TEXT PRIMARY KEY NOT NULL,
                password TEXT,
                filename TEXT,
                place TEXT,
                location TEXT,
                phone INTEGER,
                start TEXT,
                stop TEXT,
                email TEXT,
                role TEXT,
                name TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                username TEXT PRIMARY KEY NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS feedback (
                place TEXT,
                rest TEXT,
                username TEXT,
                message TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS search (
                item TEXT NOT NULL,
                def TEXT, 
                price INTEGER NOT NULL,
                category TEXT,
                place TEXT, 
                rest TEXT,
                dish_image TEXT,
				company TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS managers (
                username TEXT PRIMARY KEY NOT NULL,
                password TEXT,
                filename TEXT,
                place TEXT,
                location TEXT,
                phone INTEGER,
                start TEXT,
                stop TEXT,
                email TEXT,
                role TEXT,
                name TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                username TEXT,
                subject TEXT,
                message TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS most_ordered (
                place TEXT,
                rest TEXT,
                item TEXT,
                orders INTEGER,
                dish_image TEXT,
                price TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS notification (
                place TEXT,
                rest TEXT,
                message TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rating (
                place TEXT NOT NULL,
                rest TEXT,
                username TEXT,
                stars INTEGER
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS response (
                username TEXT,
                sub TEXT,
                message TEXT,
                sender TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                rest TEXT,
                place TEXT,
                date TEXT,
                rating INTEGER,
                review TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                item TEXT,
                price INTEGER,
                qty INTEGER,
                total INTEGER,
                place TEXT,
                rest TEXT,
                dish_image TEXT,
                phone TEXT,
                date TEXT,
                status TEXT,
                approve TEXT,
                id INTEGER PRIMARY KEY AUTOINCREMENT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS promotion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fname TEXT,
                lastname TEXT,
                amount TEXT,
                method TEXT,
                username TEXT,
                status TEXT,
                filename TEXT,
                location TEXT,
                company TEXT
            )
        ''')

        db.commit()

#homepage

@app.route('/')
def homepage():
    """Render the homepage based on the user's session status."""
    if 'username' in session and session["username"] != "admin11":
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM promotion WHERE status='1'")
        promotions = cur.fetchall()
        conn.close()
        return render_template('homepage_customer.html', promotions=promotions)
    return render_template('homepage.html')

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("homepage"))

@app.route('/privacy_policy')
def privacy_policy():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")
    varc = cur.fetchall()
    cur.execute("SELECT * FROM managers")
    varm = cur.fetchall()
    conn.close()
    
    path = '/'
    if 'username' in session:
        username = session['username']
        if any(username == x[0] for x in varc):
            path = '/homepage_customer'
        elif any(username == x[0] for x in varm):
            path = f'/manager_homepage/{next(x[3] for x in varm if username == x[0])}'
    
    return render_template('privacy_policy.html', path=path)

@app.route('/terms')
def terms():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")
    varc = cur.fetchall()
    cur.execute("SELECT * FROM managers")
    varm = cur.fetchall()
    conn.close()
    
    path = '/'
    if 'username' in session:
        username = session['username']
        if any(username == x[0] for x in varc):
            path = '/homepage_customer'
        elif any(username == x[0] for x in varm):
            path = f'/manager_homepage/{next(x[3] for x in varm if username == x[0])}'
    
    return render_template('terms.html', path=path)

@app.route('/about')
def about():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")
    varc = cur.fetchall()
    cur.execute("SELECT * FROM managers")
    varm = cur.fetchall()
    conn.close()
    
    path = '/'
    if 'username' in session:
        username = session['username']
        if any(username == x[0] for x in varc):
            path = '/homepage_customer'
        elif any(username == x[0] for x in varm):
            path = f'/manager_homepage/{next(x[3] for x in varm if username == x[0])}'
    
    return render_template('about.html', path=path)

@app.route('/security')
def security():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")
    varc = cur.fetchall()
    cur.execute("SELECT * FROM managers")
    varm = cur.fetchall()
    conn.close()
    
    path = '/'
    if 'username' in session:
        username = session['username']
        if any(username == x[0] for x in varc):
            path = '/homepage_customer'
        elif any(username == x[0] for x in varm):
            path = f'/manager_homepage/{next(x[3] for x in varm if username == x[0])}'
    
    return render_template('security.html', path=path)

@app.route('/help')
def help():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")
    varc = cur.fetchall()
    cur.execute("SELECT * FROM managers")
    varm = cur.fetchall()
    conn.close()
    
    path = '/'
    if 'username' in session:
        username = session['username']
        if any(username == x[0] for x in varc):
            path = '/homepage_customer'
        elif any(username == x[0] for x in varm):
            path = f'/manager_homepage/{next(x[3] for x in varm if username == x[0])}'
    
    return render_template('help.html', path=path)

@app.route('/contact')
def contact():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")
    varc = cur.fetchall()
    cur.execute("SELECT * FROM managers")
    varm = cur.fetchall()
    conn.close()
    
    path = '/'
    if 'username' in session:
        username = session['username']
        if any(username == x[0] for x in varc):
            path = '/homepage_customer'
        elif any(username == x[0] for x in varm):
            path = f'/manager_homepage/{next(x[3] for x in varm if username == x[0])}'
    
    return render_template('contact.html', path=path)

@app.route('/contact_form')
def contact_form():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")
    varc = cur.fetchall()
    cur.execute("SELECT * FROM managers")
    varm = cur.fetchall()
    conn.close()
    
    path = '/'
    temp = "unknown"
    if 'username' in session:
        username = session['username']
        if any(username == x[0] for x in varc):
            path = '/homepage_customer'
            temp = "customer"
        elif any(username == x[0] for x in varm):
            path = f'/manager_homepage/{next(x[3] for x in varm if username == x[0])}'
            temp = x[3]
    
    return render_template('contact_form.html', path=path, temp=temp)

@app.route('/contact_form_submitted/<temp>', methods=['GET', 'POST'])
def contact_form_submitted(temp):
    subject = request.form['subject']
    message = request.form['message']
    conn = get_db()
    cur = conn.cursor()
    
    if 'username' in session:
        username = session['username']
    else:
        username = 'unknown'
    
    cur.execute("INSERT INTO messages(username, subject, message) VALUES (%s, %s, %s)", (username, subject, message))
    conn.commit()
    conn.close()
    
    if temp == 'unknown':
        return redirect(url_for('homepage'))
    elif temp == 'customer':
        return redirect(url_for('homepage_customer'))
    else:
        return redirect(url_for('manager_homepage', place=temp))

@app.route("/signup_customer")
def signup_customer():
    return render_template('customer_signup.html')

@app.route('/customer')
def customer():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM customers")
    var = cur.fetchall()
    conn.close()
    return render_template('customer.html', var=var)

@app.route('/customer_logged_in', methods=['GET', 'POST'])
def customer_logged_in():
    session['username'] = request.form['username']
    return redirect(url_for('homepage_customer'))

@app.route('/customer_signed_up', methods=['GET', 'POST'])
def customer_signed_up():
    session['username'] = request.form['username']
    password = request.form['password']
    conn = get_db()
    cur = conn.cursor()
    
    cur.execute("INSERT INTO customers(username, password) VALUES (%s, %s)", (session['username'], password))
    cur.execute(f"CREATE TABLE IF NOT EXISTS _{session['username']}(item TEXT NOT NULL, price INTEGER, qty TEXT, total INTEGER, place TEXT, rest TEXT, dish_image TEXT)")
    cur.execute(f"CREATE TABLE IF NOT EXISTS {session['username']}_orders(item TEXT NOT NULL, price INTEGER, qty TEXT, total INTEGER, place TEXT, rest TEXT, dish_image TEXT, date TEXT)")
    conn.commit()
    conn.close()
    
    return redirect(url_for('homepage_customer'))
from flask import Flask, render_template, request, redirect, url_for, session
import psycopg2
from psycopg2 import sql
import collections

 # Replace with your actual secret key

def get_db():
    return psycopg2.connect(
        dbname='tastyh',
        user='tastyh_user',
        password='8YHmGY3f9YwCHXsC3AoIRbJNcO7m0NzA',
        host='dpg-cqohq7tsvqrc73fh9hhg-a.oregon-postgres.render.com',
        port='5432'
    )

@app.route('/customer_logout')
def customer_logout():
    session.pop('username', None)
    return redirect(url_for('homepage_customer'))

@app.route('/homepage_customer')
def homepage_customer():
    conn = get_db()
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM response WHERE username=%s", (session.get('username', None),))
        response = cur.fetchall()
        
        cur.execute("SELECT * FROM most_ordered ORDER BY orders DESC LIMIT 4")
        most_ordered = cur.fetchall()
    
    finally:
        cur.close()
        conn.close()
    
    return render_template('homepage_customer.html', response=response, most_ordered=most_ordered)

@app.route('/remove_response')
def remove_response():
    conn = get_db()
    cur = conn.cursor()
    
    try:
        cur.execute("DELETE FROM response WHERE username=%s", (session.get('username', None),))
        conn.commit()
    
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('homepage_customer'))

@app.route('/search', methods=['GET', 'POST'])
def search():
    data = request.form.get('data', '')
    conn = get_db()
    cur = conn.cursor()
    
    try:
        cur.execute("DELETE FROM search")
        
        for place in ['Accra', 'Kumasi', 'Takoradi']:
            cur.execute("SELECT username FROM managers WHERE place=%s", (place,))
            usernames = cur.fetchall()
            
            for username in usernames:
                query = sql.SQL("SELECT * FROM {} WHERE item ILIKE %s").format(
                    sql.Identifier(username[0])
                )
                cur.execute(query, ('%' + data + '%',))
                results = cur.fetchall()
                
                for result in results:
                    cur.execute("""
                        INSERT INTO search (item, def, price, category, place, rest, dish_image, company)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
                    """, (result[0], result[1], result[2], result[3], place, username[0], result[4], result[6]))
        
        conn.commit()
    
    except Exception as e:
        print(f"An error occurred: {e}")
        conn.rollback()
    
    finally:
        cur.close()
        conn.close()
    
    return redirect(url_for('search_result', data=data))

@app.route('/search_report', methods=['GET', 'POST'])
def search_report():
    if 'username' not in session:
        return "Unauthorized access"
    
    username = session['username']
    new_orders = 0
    
    if request.method == 'POST':
        date = request.form.get('date', '')
        conn = get_db()
        cur = conn.cursor()
        
        try:
            cur.execute("SELECT count(*) FROM orders WHERE status=%s AND rest=%s", ('new', username))
            new_orders = cur.fetchone()[0]
            
            cur.execute("SELECT * FROM orders WHERE rest LIKE %s AND date LIKE %s AND approve='Approved'", (f'%{username}%', date))
            rows = cur.fetchall()
            
            totalAmount = sum(row[3] for row in rows)
        
        except psycopg2.Error as e:
            print(f"PostgreSQL error: {e}")
            return "Database error occurred"
        
        finally:
            cur.close()
            conn.close()
        
        return render_template("sales_report.html", var=rows, totalAmount=totalAmount, date=date, new_orders=new_orders)
    
    return render_template("noreport.html", new_orders=new_orders)

@app.route('/search_result/<data>')
def search_result(data):
    conn = get_db()
    cur = conn.cursor()
    dict = {}
    
    try:
        cur.execute("SELECT * FROM search")
        var = cur.fetchall()
        
        cur.execute("SELECT * FROM managers WHERE username ILIKE %s", (f'%{data}%',))
        var_rest = cur.fetchall()
        
        for rest in var_rest:
            cur.execute("SELECT count(*) FROM rating WHERE place=%s AND rest=%s", (rest[3], rest[0]))
            count = cur.fetchone()[0]
            
            cur.execute("SELECT stars FROM rating WHERE place=%s AND rest=%s", (rest[3], rest[0]))
            total_stars = cur.fetchall()
            
            sum_stars = sum(star[0] for star in total_stars)
            average_stars = sum_stars / count if count > 0 else 0
            
            dict[(rest[0], rest[3])] = average_stars
    
    finally:
        cur.close()
        conn.close()
    
    return render_template('search_result.html', var=var, var_rest=var_rest, data=data, dict=dict)

@app.route('/search_result_sort/<sort>/<data>')
def search_result_sort(sort, data):
    conn = get_db()
    cur = conn.cursor()
    dict = {}
    
    try:
        order_by = {
            'desc': 'price DESC',
            'asc': 'price',
            'AtoZ': 'item',
            'ZtoA': 'item DESC'
        }.get(sort, 'item')
        
        cur.execute(f"SELECT * FROM search ORDER BY {order_by}")
        var = cur.fetchall()
        
        cur.execute("SELECT * FROM managers WHERE username ILIKE %s", (f'%{data}%',))
        var_rest = cur.fetchall()
        
        for rest in var_rest:
            cur.execute("SELECT count(*) FROM rating WHERE place=%s AND rest=%s", (rest[3], rest[0]))
            count = cur.fetchone()[0]
            
            cur.execute("SELECT stars FROM rating WHERE place=%s AND rest=%s", (rest[3], rest[0]))
            total_stars = cur.fetchall()
            
            sum_stars = sum(star[0] for star in total_stars)
            average_stars = sum_stars / count if count > 0 else 0
            
            dict[(rest[0], rest[3])] = average_stars
    
    finally:
        cur.close()
        conn.close()
    
    return render_template('search_result.html', var=var, var_rest=var_rest, data=data, dict=dict)

@app.route('/search_result_sort_rest/<sort>/<data>')
def search_result_sort_rest(sort, data):
    conn = get_db()
    cur = conn.cursor()
    dict = {}
    
    try:
        if sort == 'asc':
            cur.execute("SELECT * FROM managers WHERE username ILIKE %s ORDER BY username", (f'%{data}%',))
        elif sort == 'desc':
            cur.execute("SELECT * FROM managers WHERE username ILIKE %s ORDER BY username DESC", (f'%{data}%',))
        elif sort == 'rating':
            cur.execute("SELECT * FROM managers WHERE username ILIKE %s", (f'%{data}%',))
            var_rest = cur.fetchall()
            for rest in var_rest:
                cur.execute("SELECT count(*) FROM rating WHERE place=%s AND rest=%s", (rest[3], rest[0]))
                count = cur.fetchone()[0]
                
                cur.execute("SELECT stars FROM rating WHERE place=%s AND rest=%s", (rest[3], rest[0]))
                total_stars = cur.fetchall()
                
                sum_stars = sum(star[0] for star in total_stars)
                average_stars = sum_stars / count if count > 0 else 0
                
                dict[rest[0]] = average_stars
            
            ord_dict = collections.OrderedDict(sorted(dict.items(), key=lambda x: x[1], reverse=True))
            return render_template('search_result_rating.html', var_rest=var_rest, data=data, ord_dict=ord_dict)
        
        else:
            cur.execute("SELECT * FROM managers WHERE username ILIKE %s", (f'%{data}%',))
        
        var_rest = cur.fetchall()
        for rest in var_rest:
            cur.execute("SELECT count(*) FROM rating WHERE place=%s AND rest=%s", (rest[3], rest[0]))
            count = cur.fetchone()[0]
            
            cur.execute("SELECT stars FROM rating WHERE place=%s AND rest=%s", (rest[3], rest[0]))
            total_stars = cur.fetchall()
            
            sum_stars = sum(star[0] for star in total_stars)
            average_stars = sum_stars / count if count > 0 else 0
            
            dict[rest[0]] = average_stars
    
    finally:
        cur.close()
        conn.close()
    
    return render_template('search_result.html', var_rest=var_rest, data=data, dict=dict)

@app.route('/<place>')
def location(place):
    conn = get_db()
    cur = conn.cursor()
    dict = {}
    
    try:
        cur.execute("SELECT username FROM managers WHERE place=%s", (place,))
        managers = cur.fetchall()
        
        for manager in managers:
            cur.execute("SELECT count(*) FROM rating WHERE place=%s AND rest=%s", (place, manager[0]))
            count = cur.fetchone()[0]
            
            cur.execute("SELECT stars FROM rating WHERE place=%s AND rest=%s", (place, manager[0]))
            total_stars = cur.fetchall()
            
            sum_stars = sum(star[0] for star in total_stars)
            average_stars = sum_stars / count if count > 0 else 0
            
            dict[manager[0]] = average_stars
    
    finally:
        cur.close()
        conn.close()
    
    return render_template('locations.html', location=place, dict=dict)


#to access different menus of restaurants

def get_db_connection(place=None):
    """Establish and return a database connection based on the place."""
    if place in ['Accra', 'Kumasi']:
        conn = sqlite3.connect(f'{place}.db')
        conn.row_factory = sqlite3.Row
    else:
        conn = psycopg2.connect(
            dbname='tastyh',
            user='tastyh_user',
            password='8YHmGY3f9YwCHXsC3AoIRbJNcO7m0NzA',
            host='dpg-cqohq7tsvqrc73fh9hhg-a.oregon-postgres.render.com',
            port='5432'
        )
    return conn

@app.route('/<place>/menu/<rest>')
def menu(place, rest):
    conn = get_db_connection(place)
    cur = conn.cursor()
    
    try:
        cur.execute(f"SELECT COUNT(*) FROM {rest}")
        if cur.fetchone()[0] > 0:
            categories = ['veg', 'non-veg', 'others']
            menu_items = {}
            
            for category in categories:
                cur.execute(f"SELECT * FROM {rest} WHERE category=%s", (category,))
                menu_items[category] = cur.fetchall()
            
            if conn.dsn:
                conn.close()  # Close SQLite connection if used

            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("SELECT * FROM managers WHERE place=%s AND username=%s", (place, rest))
            temp = cur.fetchone()

            cur.execute("SELECT stars FROM rating WHERE place=%s AND rest=%s AND username=%s", (place, rest, session.get('username')))
            var_stars = cur.fetchone()

            cur.execute("SELECT COUNT(*) FROM rating WHERE place=%s AND rest=%s", (place, rest))
            count = cur.fetchone()[0]

            cur.execute("SELECT stars FROM rating WHERE place=%s AND rest=%s", (place, rest))
            total_stars = cur.fetchall()
            sum_stars = sum(star[0] for star in total_stars)
            average_stars = sum_stars / count if count > 0 else 0

            return render_template('menu.html', **menu_items, place=place, rest=rest, temp=temp, var_stars=var_stars, sum=average_stars)

        return render_template('nomenu.html', place=place)
    
    finally:
        cur.close()
        conn.close()

@app.route('/<place>/<rest>/rating/<stars>')
def rating(place, rest, stars):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            INSERT INTO rating (place, rest, username, stars)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (place, rest, username) DO UPDATE
            SET stars = EXCLUDED.stars
        """, (place, rest, session['username'], stars))
        
        cur.execute("""
            INSERT INTO reviews (place, rest, username, rating)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (place, rest, username) DO UPDATE
            SET rating = EXCLUDED.rating
        """, (place, rest, session['username'], stars))

        conn.commit()
        return redirect(url_for('menu', place=place, rest=rest))
    
    finally:
        cur.close()
        conn.close()

@app.route('/<place>/<rest>/rating_change/<stars>')
def rating_change(place, rest, stars):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            UPDATE rating SET stars = %s
            WHERE place = %s AND rest = %s AND username = %s
        """, (stars, place, rest, session['username']))

        cur.execute("""
            UPDATE reviews SET rating = %s
            WHERE place = %s AND rest = %s AND username = %s
        """, (stars, place, rest, session['username']))

        conn.commit()
        return redirect(url_for('menu', place=place, rest=rest))
    
    finally:
        cur.close()
        conn.close()

@app.route('/<place>/menu/<rest>/<sort>')
def menu_sort(place, rest, sort):
    conn = get_db_connection(place)
    cur = conn.cursor()
    
    try:
        order_by = {
            "nameasc": "item ASC",
            "namedes": "item DESC",
            "pricelh": "price ASC",
            "pricehl": "price DESC"
        }.get(sort, "item ASC")
        
        cur.execute(f"SELECT COUNT(*) FROM {rest}")
        if cur.fetchone()[0] > 0:
            categories = ['veg', 'non-veg', 'others']
            menu_items = {}
            
            for category in categories:
                cur.execute(f"SELECT * FROM {rest} WHERE category=%s ORDER BY {order_by}", (category,))
                menu_items[category] = cur.fetchall()
            
            if conn.dsn:
                conn.close()  # Close SQLite connection if used

            conn = get_db_connection()
            cur = conn.cursor()

            cur.execute("SELECT * FROM managers WHERE place=%s AND username=%s", (place, rest))
            temp = cur.fetchone()

            cur.execute("SELECT stars FROM rating WHERE place=%s AND rest=%s AND username=%s", (place, rest, session.get('username')))
            var_stars = cur.fetchone()

            cur.execute("SELECT COUNT(*) FROM rating WHERE place=%s AND rest=%s", (place, rest))
            count = cur.fetchone()[0]

            cur.execute("SELECT stars FROM rating WHERE place=%s AND rest=%s", (place, rest))
            total_stars = cur.fetchall()
            sum_stars = sum(star[0] for star in total_stars)
            average_stars = sum_stars / count if count > 0 else 0

            return render_template('menu.html', **menu_items, place=place, rest=rest, temp=temp, var_stars=var_stars, sum=average_stars)
        
        return render_template('nomenu.html', place=place)
    
    finally:
        cur.close()
        conn.close()

@app.route('/quantity/<place>/<rest>/<item>/<price>/<dish_image>', methods=['GET', 'POST'])
def quantity(place, rest, item, price, dish_image):
    return render_template('quantity.html', item=item, price=price, place=place, rest=rest, dish_image=dish_image)

@app.route('/postquantity/<place>/<rest>/<item>/<price>/<dish_image>', methods=['POST'])
def postquantity(place, rest, item, price, dish_image):
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        qty = request.form['qty']
        total = int(price) * int(qty)
        table_name = f"_{session['username']}"

        cur.execute(f"""
            INSERT INTO {table_name} (item, price, qty, total, place, rest, dish_image)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (item, place, rest) DO UPDATE
            SET qty = qty + EXCLUDED.qty, total = qty * price
        """, (item, price, qty, total, place, rest, dish_image))
        
        conn.commit()
        return redirect(url_for('homepage_customer'))
    
    finally:
        cur.close()
        conn.close()

@app.route("/add_quantity/<id>")
def add_quantity(id):
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()
    
    table_name = f"_{session['username']}"
    
    try:
        cur.execute(f"SELECT * FROM {table_name} WHERE id=?", (id,))
        if cur.fetchone():
            cur.execute(f"""
                UPDATE {table_name} SET qty = qty + 1, total = qty * price
                WHERE id = ?
            """, (id,))
            conn.commit()
        return redirect(url_for('cartshow'))
    
    finally:
        cur.close()
        conn.close()

@app.route("/approve_order/<id>")
def approve_order(id):
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM orders WHERE id=?", (id,))
        if cur.fetchone():
            cur.execute("UPDATE orders SET approve = 'Approved' WHERE id = ?", (id,))
            conn.commit()
        return redirect(url_for('m_orders'))
    
    finally:
        cur.close()
        conn.close()

@app.route("/cancel_order/<id>")
def cancel_order(id):
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()
    
    try:
        cur.execute("SELECT * FROM orders WHERE id=?", (id,))
        if cur.fetchone():
            cur.execute("UPDATE orders SET approve = 'Cancelled' WHERE id = ?", (id,))
            conn.commit()
        return redirect(url_for('m_orders'))
    
    finally:
        cur.close()
        conn.close()

@app.route("/reset_password", methods=["POST"])
def reset_password():
    """Reset the password for a user."""
    username = request.form.get("username")
    new_password = request.form.get("new_password")

    if not username or not new_password:
        flash("Username and new password are required!", "error")
        return redirect(url_for('homepage_customer'))

    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        cur.execute("""
            UPDATE users SET password = %s
            WHERE username = %s
        """, (new_password, username))
        conn.commit()
        flash("Password reset successful!", "success")
        return redirect(url_for('homepage_customer'))
    
    finally:
        cur.close()
        conn.close()



# Handle cases where the request method is not POST
@app.errorhandler(405)
def method_not_allowed(error):
    flash("Method not allowed.")
    return redirect(url_for('homepage'))





def connect_db():
    # Adjust the database path as needed
    return sqlite3.connect('members.db')

 # Set your secret key for session management

def get_db_connection():
    """Establish and return a database connection."""
    if 'username' in session:
        # Assuming different databases for different scenarios
        if session['username'] == 'admin11':
            return psycopg2.connect(
                dbname='tastyh',
                user='tastyh_user',
                password='8YHmGY3f9YwCHXsC3AoIRbJNcO7m0NzA',
                host='dpg-cqohq7tsvqrc73fh9hhg-a.oregon-postgres.render.com',
                port='5432'
            )
        else:
            return sqlite3.connect('members.db')
    return None

@app.route("/manager_logged_in", methods=['POST'])
def manager_logged_in():
    username = request.form.get('username')

    if username == "admin11":
        return redirect(url_for('admin'))

    conn = get_db_connection()
    cur = conn.cursor()

    try:
        # Check for active promotions
        cur.execute("SELECT * FROM promotion WHERE status='1'")
        promotions = cur.fetchall()

        # Check if the username exists in the managers table and get the place
        cur.execute("SELECT place FROM managers WHERE username=?", (username,))
        place = cur.fetchone()

        if place:
            session['username'] = username
            return redirect(url_for('manager_homepage', place=place[0]))

        # If username is not found in managers table, check the customers table
        cur.execute("SELECT * FROM customers WHERE username=?", (username,))
        customer = cur.fetchone()

        if customer:
            session['username'] = username
            return render_template('homepage_customer.html', promotions=promotions)

        flash("Username not found in the database")
        return redirect(url_for('homepage'))

    finally:
        cur.close()
        conn.close()

@app.route("/approve_advert/<id>")
def approve_advert(id):
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM promotion WHERE id=?", (id,))
        if cur.fetchone():
            cur.execute("UPDATE promotion SET status = '1' WHERE id = ?", (id,))
            conn.commit()
        return redirect(url_for('advert'))

    finally:
        cur.close()
        conn.close()

@app.route("/cancel_advert/<id>")
def cancel_advert(id):
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM promotion WHERE id=?", (id,))
        if cur.fetchone():
            cur.execute("UPDATE promotion SET status = '0' WHERE id = ?", (id,))
            conn.commit()
        return redirect(url_for('advert'))

    finally:
        cur.close()
        conn.close()

@app.route("/cancel_order_customer/<id>")
def cancel_order_customer(id):
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM orders WHERE id=?", (id,))
        if cur.fetchone():
            cur.execute("UPDATE orders SET approve = 'Cancelled' WHERE id = ?", (id,))
            conn.commit()
        return redirect(url_for('orders'))

    finally:
        cur.close()
        conn.close()

@app.route("/remove_quantity/<id>")
def remove_quantity(id):
    find_table = "_" + session["username"]
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM {find_table} WHERE id=?", (id,))
        if cur.fetchone():
            cur.execute(f"UPDATE {find_table} SET qty = qty - 1 WHERE id = ?", (id,))
            cur.execute(f"UPDATE {find_table} SET total = qty * price WHERE id = ?", (id,))
            conn.commit()
        return redirect(url_for('cartshow'))

    finally:
        cur.close()
        conn.close()

@app.route('/cartshow')
def cartshow():
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM managers")
        managers = cur.fetchall()

        user_table = f"_{session['username']}"
        cur.execute(f"SELECT COUNT(*) FROM {user_table}")
        item_count = cur.fetchone()[0]

        if item_count > 0:
            cur.execute(f"SELECT * FROM {user_table}")
            cart_items = cur.fetchall()
            return render_template('cartshow.html', var=cart_items, var2=managers)
        else:
            return render_template("nocart.html")

    except Exception as e:
        print(f"Error in cartshow: {e}")
        return f"Error in cartshow: {e}"

    finally:
        cur.close()
        conn.close()

@app.route('/cartremove/<item>/<place>/<rest>/<qty>')
def cartremove(item, place, rest, qty):
    conn = psycopg2.connect(
        dbname='tastyh',
        user='tastyh_user',
        password='8YHmGY3f9YwCHXsC3AoIRbJNcO7m0NzA',
        host='dpg-cqohq7tsvqrc73fh9hhg-a.oregon-postgres.render.com',
        port='5432'
    )
    cur = conn.cursor()

    try:
        user_table = f"_{session['username']}"
        cur.execute(f"SELECT COUNT(*) FROM {user_table}")
        item_count = cur.fetchone()[0]

        if item_count > 0:
            cur.execute(f"DELETE FROM {user_table} WHERE item=%s AND place=%s AND qty=%s", (item, place, qty))
            conn.commit()
        return redirect(url_for('cartshow'))

    finally:
        cur.close()
        conn.close()

@app.route('/cartpay')
def cartpay():
    return render_template('cartpay.html')

@app.route('/paycard')
def paycard():
    return render_template('paycard.html')

@app.route('/cartclear')
def cartclear():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    orders_table = f"_{username}_orders"
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    conn = sqlite3.connect('members.db')
    cur = conn.cursor()

    try:
        cur.execute(f"SELECT * FROM _{username}")
        cart_items = cur.fetchall()

        for item in cart_items:
            cur.execute(f"INSERT INTO {orders_table} VALUES(?,?,?,?,?,?,?,?)",
                        (item[0], item[1], item[2], item[3], item[4], item[5], item[6], current_date))
            cur.execute("INSERT INTO orders(item, price, qty, total, place, rest, dish_image, phone, date, status, approve) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                        (item[0], item[1], item[2], item[3], item[4], item[5], item[6], username, current_date, "new", "Pending"))
            
            cur.execute("SELECT * FROM managers WHERE username=?", (item[5],))
            manager = cur.fetchone()
            if manager and len(manager) > 8:
                manager_email = manager[8]
                # send_email(manager_email, "New Order Notification")
                
            cur.execute("SELECT * FROM most_ordered WHERE place=? AND rest=? AND item=?", (item[4], item[5], item[0]))
            most_ordered = cur.fetchone()
            if most_ordered:
                cur.execute("UPDATE most_ordered SET orders=orders+? WHERE place=? AND rest=? AND item=?", (item[2], item[4], item[5], item[0]))
            else:
                cur.execute("INSERT INTO most_ordered VALUES(?,?,?,?,?,?)", (item[4], item[5], item[0], item[2], item[6], item[1]))

        cur.execute("INSERT INTO response VALUES(?,?,?,?)", (username, 'confirmation', 'order confirmed', 'admin'))
        cur.execute(f"DELETE FROM _{username}")

        conn.commit()

    except sqlite3.Error as e:
        print(f"SQLite error in cartclear: {e}")

    finally:
        cur.close()
        conn.close()

    return redirect(url_for('orders'))

@app.route('/orders')
def orders():
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM orders WHERE phone=? ORDER BY date DESC", (session['username'],))
        orders = cur.fetchall()
        return render_template('orders.html', var=orders) if orders else render_template('no_orders.html')

    finally:
        cur.close()
        conn.close()

@app.route('/m_orders')
def m_orders():
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()

    try:
        cur.execute("UPDATE orders SET status = 'old' WHERE rest = ?", (session['username'],))
        conn.commit()
        cur.execute("SELECT * FROM orders WHERE rest = ? ORDER BY date DESC", (session['username'],))
        orders = cur.fetchall()

        cur.execute("SELECT count(*) FROM orders WHERE status='new' AND rest=?", (session['username'],))
        new_orders_count = cur.fetchone()[0]

        return render_template('manager_order.html', var=orders, new_orders=new_orders_count) if orders else render_template('no_orders.html')

    finally:
        cur.close()
        conn.close()

@app.route('/feedback/<place>/<rest>', methods=['POST'])
def feedback(place, rest):
    conn = psycopg2.connect(
        dbname='tastyh',
        user='tastyh_user',
        password='8YHmGY3f9YwCHXsC3AoIRbJNcO7m0NzA',
        host='dpg-cqohq7tsvqrc73fh9hhg-a.oregon-postgres.render.com',
        port='5432'
    )
    cur = conn.cursor()

    try:
        message = request.form['message']
        cur.execute("INSERT INTO feedback (place, rest, username, message) VALUES (%s, %s, %s, %s)",
                    (place, rest, session['username'], message))
        conn.commit()
        return redirect(url_for('menu', place=place, rest=rest))

    finally:
        cur.close()
        conn.close()

@app.route('/reviews/<place>/<rest>')
def reviews(place, rest):
    conn = psycopg2.connect(
        dbname='tastyh',
        user='tastyh_user',
        password='8YHmGY3f9YwCHXsC3AoIRbJNcO7m0NzA',
        host='dpg-cqohq7tsvqrc73fh9hhg-a.oregon-postgres.render.com',
        port='5432'
    )
    cur = conn.cursor()

    try:
        cur.execute("SELECT * FROM reviews WHERE place=%s AND rest=%s", (place, rest))
        reviews_list = cur.fetchall()
        return render_template('reviews.html', place=place, rest=rest, reviews=reviews_list)

    finally:
        cur.close()
        conn.close()



#to insert review in reviews table


# Database configuration
DATABASE_CONFIG = {
    'dbname': 'tastyh',
    'user': 'tastyh_user',
    'password': '8YHmGY3f9YwCHXsC3AoIRbJNcO7m0NzA',
    'host': 'dpg-cqohq7tsvqrc73fh9hhg-a.oregon-postgres.render.com',
    'port': '5432'
}

# Folder configuration

def get_db_connection():
    return psycopg2.connect(**DATABASE_CONFIG)

@app.route('/review_post/<place>/<rest>', methods=['GET', 'POST'])
def review_post(place, rest):
    conn = get_db_connection()
    cur = conn.cursor()
    
    review = request.form['review']
    date = time.strftime("%x")
    username = session.get('username')
    
    cur.execute("SELECT stars FROM rating WHERE place=%s AND rest=%s AND username=%s", (place, rest, username))
    stars = cur.fetchone()
    
    if stars is None:
        cur.execute("INSERT INTO reviews (username, rest, place, date, rating, review) VALUES (%s, %s, %s, %s, %s, %s)", 
                    (username, rest, place, date, 0, review))
    else:
        cur.execute("INSERT INTO reviews (username, rest, place, date, rating, review) VALUES (%s, %s, %s, %s, %s, %s)", 
                    (username, rest, place, date, stars[0], review))
    
    conn.commit()
    conn.close()
    return redirect(url_for('reviews', place=place, rest=rest))

@app.route('/manager_login', methods=['GET', 'POST'])
def manager_login():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM managers")
    managers = cur.fetchall()
    conn.close()
    return render_template('manager_login.html', var=managers)

@app.route('/manager_signup')
def manager_signup():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT username, place FROM managers")
    managers = cur.fetchall()
    cur.execute("SELECT username, place FROM approval")
    approvals = cur.fetchall()
    
    conn.close()
    return render_template('manager_signup.html', var=managers, approval=approvals)

@app.route('/manager_signed_up', methods=['GET', 'POST'])
def manager_signed_up():
    place = request.form['place']
    username = request.form['username']
    password = request.form['password']
    location = request.form['location']
    phone = request.form['phone']
    start_time = request.form['start_time']
    close_time = request.form['close_time']
    email = request.form["email"]
    name = request.form["restaurant_name"]
    roles = "manager"
    
    file = request.files['filename']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER_REST'], filename))
    
    source = os.path.join(app.config['UPLOAD_FOLDER_REST'], filename)
    destination = os.path.join(app.config['UPLOAD_FOLDER_REST'], f"{place}_{username}.jpg")
    os.rename(source, destination)
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("INSERT INTO approval (username, password, filename, place, location, phone, start, stop, email, role, name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (username, password, f"{place}_{username}.jpg", place, location, phone, start_time, close_time, email, roles, name))
    
    conn.commit()
    conn.close()
    return render_template('manager_processing.html')

@app.route('/manager_logout')
def manager_logout():
    session.pop('username', None)
    return redirect(url_for('homepage'))

@app.route("/forget_password")
def forget_password():
    session.pop("username", None)
    return render_template("forget.html")

@app.route('/manager_homepage/<place>', methods=['GET', 'POST'])
def manager_homepage(place):
    db_file = f"{place}.db" if place in ['Accra', 'Kumasi'] else 'location.db'
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    
    username = session.get('username')
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()
    
    conn.close()
    return redirect(url_for('manager_menu', place=place, username=username))

@app.route('/go_manager')
def go_manager():
    username = session.get("username")
    if username is None:
        return redirect(url_for('login'))

    conn = sqlite3.connect('members.db')
    cur = conn.cursor()
    cur.execute("SELECT place FROM managers WHERE username=?", (username,))
    place_row = cur.fetchone()
    conn.close()

    if place_row is None:
        return redirect(url_for('error_page'))

    place = place_row[0]
    return redirect(url_for('manager_homepage', place=place))

@app.route('/manager_menu/<place>/<username>')
def manager_menu(place, username):
    db_file = f"{place}.db" if place in ['Accra', 'Kumasi'] else 'location.db'
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()
    
    cur.execute(f"SELECT * FROM {username}")
    menu_items = cur.fetchall()
    conn.close()

    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM notification WHERE place=%s AND rest=%s", (place, username))
    notifications = cur.fetchall()
    
    cur.execute("SELECT * FROM feedback WHERE place=%s AND rest=%s", (place, username))
    feedbacks = cur.fetchall()
    
    cur.execute("SELECT * FROM managers WHERE username=%s AND place=%s", (username, place))
    manager_info = cur.fetchone()
    
    cur.execute("SELECT stars FROM rating WHERE place=%s AND rest=%s", (place, username))
    total_stars = cur.fetchall()
    
    cur.execute("SELECT count(*) FROM rating WHERE place=%s AND rest=%s", (place, username))
    count = cur.fetchone()
    
    cur.execute("SELECT count(*) FROM orders WHERE status=%s AND rest=%s", ('new', username))
    new_orders = cur.fetchone()[0]
    
    conn.close()
    
    average_stars = sum(x[0] for x in total_stars) / count[0] if count[0] != 0 else 0
    return render_template('manager_menu.html', new_orders=new_orders, var=menu_items, var1=manager_info, place=place, username=username, sum=average_stars, feedbacks=feedbacks, notification=notifications)

@app.route('/manager_edit_restaurant_form/<place>/<username>/<loc>/<ph>/<st>/<ct>/<di>')
def manager_edit_restaurant_form(place, username, loc, ph, st, ct, di):
    return render_template('manager_edit_restaurant_form.html', place=place, username=username, loc=loc, ph=ph, st=st, ct=ct, di=di)

@app.route('/manager_edit_restaurant/<place>/<username>', methods=['GET', 'POST'])
def manager_edit_restaurant(place, username):
    location = request.form['location']
    phone = request.form['phone']
    start_time = request.form['start_time']
    close_time = request.form['close_time']
    
    file = request.files['filename']
    if file:
        filename = secure_filename(file.filename)
        old_image = os.path.join(app.config['UPLOAD_FOLDER_REST'], f"{place}_{username}.jpg")
        if os.path.exists(old_image):
            os.remove(old_image)
        
        file.save(os.path.join(app.config['UPLOAD_FOLDER_REST'], filename))
        source = os.path.join(app.config['UPLOAD_FOLDER_REST'], filename)
        destination = os.path.join(app.config['UPLOAD_FOLDER_REST'], f"{place}_{username}.jpg")
        os.rename(source, destination)
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE managers SET location=%s, phone=%s, start=%s, stop=%s, filename=%s WHERE place=%s AND username=%s",
                (location, phone, start_time, close_time, f"{place}_{username}.jpg", place, username))
    conn.commit()
    conn.close()
    
    return redirect(url_for('manager_homepage', place=place))

@app.route('/manager_edit/<place>/<username>/<action>', methods=['GET', 'POST'])
def manager_edit(place, username, action):
    if action == "add":
        db_file = f"{place}.db" if place in ['Accra', 'Kumasi'] else 'location.db'
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(f"SELECT item FROM {username}")
        items = cur.fetchall()
        conn.close()
        return render_template('manager_add.html', var=items, place=place, username=username)
    elif action == "update":
        db_file = f"{place}.db" if place in ['Accra', 'Kumasi'] else 'location.db'
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(f"SELECT item FROM {username}")
        items = cur.fetchall()
        conn.close()
        return render_template('manager_update.html', var=items, place=place, username=username)
    elif action == "delete":
        db_file = f"{place}.db" if place in ['Accra', 'Kumasi'] else 'location.db'
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        cur.execute(f"SELECT item FROM {username}")
        items = cur.fetchall()
        conn.close()
        return render_template('manager_delete.html', var=items, place=place, username=username)

@app.route('/manager_add/<place>/<username>', methods=['POST'])
def manager_add(place, username):
    item = request.form['item']
    price = request.form['price']
    conn = sqlite3.connect(f"{place}.db" if place in ['Accra', 'Kumasi'] else 'location.db')
    cur = conn.cursor()
    cur.execute(f"INSERT INTO {username} (item, price) VALUES (?, ?)", (item, price))
    conn.commit()
    conn.close()
    return redirect(url_for('manager_menu', place=place, username=username))

@app.route('/manager_update/<place>/<username>', methods=['POST'])
def manager_update(place, username):
    item = request.form['item']
    new_price = request.form['new_price']
    conn = sqlite3.connect(f"{place}.db" if place in ['Accra', 'Kumasi'] else 'location.db')
    cur = conn.cursor()
    cur.execute(f"UPDATE {username} SET price=? WHERE item=?", (new_price, item))
    conn.commit()
    conn.close()
    return redirect(url_for('manager_menu', place=place, username=username))

@app.route('/manager_delete/<place>/<username>', methods=['POST'])
def manager_delete(place, username):
    item = request.form['item']
    conn = sqlite3.connect(f"{place}.db" if place in ['Accra', 'Kumasi'] else 'location.db')
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {username} WHERE item=?", (item,))
    conn.commit()
    conn.close()
    return redirect(url_for('manager_menu', place=place, username=username))

@app.route('/admin_homepage')
def admin_homepage():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT username, place FROM approval")
    approvals = cur.fetchall()
    
    cur.execute("SELECT username, place FROM managers")
    managers = cur.fetchall()
    
    conn.close()
    return render_template('admin_homepage.html', approvals=approvals, managers=managers)

@app.route('/admin_approval/<place>/<username>')
def admin_approval(place, username):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM approval WHERE place=%s AND username=%s", (place, username))
    approval_info = cur.fetchone()
    
    conn.close()
    return render_template('admin_approval.html', var=approval_info)

@app.route('/admin_approve/<place>/<username>', methods=['POST'])
def admin_approve(place, username):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM approval WHERE place=%s AND username=%s", (place, username))
    approval_info = cur.fetchone()
    
    if approval_info:
        cur.execute("INSERT INTO managers (username, place, password, filename, location, phone, start, stop, email, role, name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (username, place, approval_info[1], approval_info[2], approval_info[3], approval_info[4], approval_info[5], approval_info[6], approval_info[7], approval_info[8], approval_info[9]))
        
        cur.execute("DELETE FROM approval WHERE place=%s AND username=%s", (place, username))
    
    conn.commit()
    conn.close()
    return redirect(url_for('admin_homepage'))

@app.route('/admin_delete/<place>/<username>', methods=['POST'])
def admin_delete(place, username):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("DELETE FROM managers WHERE place=%s AND username=%s", (place, username))
    cur.execute("DELETE FROM reviews WHERE place=%s AND username=%s", (place, username))
    cur.execute("DELETE FROM rating WHERE place=%s AND username=%s", (place, username))
    cur.execute("DELETE FROM orders WHERE place=%s AND username=%s", (place, username))
    
    conn.commit()
    conn.close()
    return redirect(url_for('admin_homepage'))





if __name__ == '__main__':
   init_db()
   app.run(debug = True)	

