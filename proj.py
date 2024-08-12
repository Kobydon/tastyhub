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

from flask import g
import sqlite3
app = Flask(__name__)
app.secret_key = 'any random string'
app.config['DATABASE'] = 'members.db'

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'jxkalmhefacbuk@gmail.com'
app.config['MAIL_PASSWORD'] ='qhsf mguh pzuh dcmx'  # or use an app-specific password
app.config['MAIL_DEFAULT_SENDER'] = 'jxkalmhefacbuk@gmail.com'

mail = Mail(app)
# Gmail SMTP configuration


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(app.config['DATABASE'])
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
    
    # Check if the user is logged in and if their username is not 'admin11'
    if 'username' in session and session["username"] != "admin11":
        # Connect to the database
        conn = connect_db()
        cur = conn.cursor()
        
        # Fetch active promotions for customers
        cur.execute("SELECT * FROM promotion WHERE status='1'")
        promotions = cur.fetchall()
        conn.close()
        
        # Render the customer homepage with promotions
        return render_template('homepage_customer.html', promotions=promotions)
    
    # Render the admin or general homepage if not a customer
    return render_template('homepage.html')

@app.route("/logout")
def logout():
    session.pop("username", None)  # Remove 'username' from session, default to None if it doesn't exist
    return redirect(url_for("homepage"))


@app.route('/privacy_policy')
def privacy_policy():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM customers")
	varc=cur.fetchall()
	cur.execute("SELECT * FROM managers")
	varm=cur.fetchall()
	conn.close()	
	if not session:
		path='/'
	else:
		for x in varc:
			if session['username']==x[0]:
				path='/homepage_customer'
		for x in varm:
			if session['username']==x[0]:
				path='/manager_homepage/'+x[3]
	return render_template('privacy_policy.html',path=path)

@app.route('/terms')
def terms():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM customers")
	varc=cur.fetchall()
	cur.execute("SELECT * FROM managers")
	varm=cur.fetchall()
	conn.close()	
	if not session:
		path='/'
	else:
		for x in varc:
			if session['username']==x[0]:
				path='/homepage_customer'
		for x in varm:
			if session['username']==x[0]:
				path='/manager_homepage/'+x[3]
	return render_template('terms.html',path=path)


@app.route('/about')
def about():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM customers")
	varc=cur.fetchall()
	cur.execute("SELECT * FROM managers")
	varm=cur.fetchall()
	conn.close()	
	if not session:
		path='/'
	else:
		for x in varc:
			if session['username']==x[0]:
				path='/homepage_customer'
		for x in varm:
			if session['username']==x[0]:
				path='/manager_homepage/'+x[3]
	return render_template('about.html',path=path)


@app.route('/security')
def security():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM customers")
	varc=cur.fetchall()
	cur.execute("SELECT * FROM managers")
	varm=cur.fetchall()
	conn.close()	
	if not session:
		path='/'
	else:
		for x in varc:
			if session['username']==x[0]:
				path='/homepage_customer'
		for x in varm:
			if session['username']==x[0]:
				path='/manager_homepage/'+x[3]
	return render_template('security.html',path=path)



@app.route('/help')
def help():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM customers")
	varc=cur.fetchall()
	cur.execute("SELECT * FROM managers")
	varm=cur.fetchall()
	conn.close()	
	if not session:
		path='/'
	else:
		for x in varc:
			if session['username']==x[0]:
				path='/homepage_customer'
		for x in varm:
			if session['username']==x[0]:
				path='/manager_homepage/'+x[3]
	return render_template('help.html',path=path)



@app.route('/contact')
def contact():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM customers")
	varc=cur.fetchall()
	cur.execute("SELECT * FROM managers")
	varm=cur.fetchall()
	conn.close()	
	if not session:
		path='/'
	else:
		for x in varc:
			if session['username']==x[0]:
				path='/homepage_customer'
		for x in varm:
			if session['username']==x[0]:
				path='/manager_homepage/'+x[3]
	return render_template('contact.html',path=path)


@app.route('/contact_form')
def contact_form():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM customers")
	varc=cur.fetchall()
	cur.execute("SELECT * FROM managers")
	varm=cur.fetchall()
	conn.close()	
	if not session:
		path='/'
		temp="unknown"
	else:
		for x in varc:
			if session['username']==x[0]:
				path='/homepage_customer'
				temp="customer"
		for x in varm:
			if session['username']==x[0]:
				path='/manager_homepage/'+x[3]
				temp=x[3]
	return render_template('contact_form.html',path=path,temp=temp)


@app.route('/contact_form_submitted/<temp>',methods=['GET','POST'])
def contact_form_submitted(temp):
	subject=request.form['subject']
	message=request.form['message']
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	if not session:
		cur.execute("INSERT INTO messages(username,subject,message) VALUES(?,?,?)",('unknown',subject,message,))
	else:
		cur.execute("INSERT INTO messages(username,subject,message) VALUES(?,?,?)",(session['username'],subject,message,))
	conn.commit()
	conn.close()
	if(temp =='unknown'):
		return redirect(url_for('homepage'))
	elif(temp=='customer'):
		return redirect(url_for('homepage_customer'))	
	else:
		return redirect(url_for('manager_homepage',place=temp))	





@app.route("/signup_customer")
def  signup_customer():
	return render_template('customer_signup.html')



#page for displaying login for customers
@app.route('/customer')
def customer():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM customers")
	var=cur.fetchall()
	conn.close()
	return render_template('customer.html',var=var)
	#from customer.html , goes to homepage_customer()

#customer session is created after log in
@app.route('/customer_logged_in',methods=['GET','POST'])
def customer_logged_in():
	session['username']=request.form['username']              #session is a dictionery with username its key.. value is nm variable
	return redirect(url_for('homepage_customer'))

#customer session created after sign up
@app.route('/customer_signed_up',methods=['GET','POST'])
def customer_signed_up():
	session['username']=request.form['username']             #session is a dictionery with username its key.. value is nm variable
	password=request.form['password']
	address = request.form["address"]
	phone = request.form["phone"]
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	
	cur.execute("INSERT INTO customers(username,password,address,phone) VALUES (?,?,?,?)",(session['username'],password,address,phone))
	cur.execute("CREATE TABLE {}(item text NOT NULL ,price INTEGER , qty TEXT ,total INTEGER , place TEXT ,rest TEXT,dish_image TEXT)".format("_"+session['username']))
	temp="_"+session['username']+'_orders'
	cur.execute("CREATE TABLE IF NOT EXISTS {}(item text NOT NULL ,price INTEGER , qty TEXT ,total INTEGER , place TEXT ,rest TEXT,dish_image TEXT,date TEXT);".format(temp))
	conn.commit()
	return redirect(url_for('homepage_customer'))


#when customer wants to logout
@app.route('/customer_logout')
def customer_logout():
	session.pop('username', None)					#used to logout of current session
	return redirect(url_for('homepage'))




#homepage of customer where restaurants are needed to be selected
@app.route('/homepage_customer')
def homepage_customer():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM response WHERE username=?",(session['username'],))
	response=cur.fetchall()
	cur.execute("SELECT * FROM most_ordered ORDER BY orders DESC limit 4")
	most_ordered=cur.fetchall()
	conn.close()
	return render_template('homepage_customer.html',response=response,most_ordered=most_ordered)







#when customer wants to remove responses
@app.route('/remove_response')	
def remove_response():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM response WHERE username=?",(session['username'],))
	conn.commit()
	conn.close()
	return redirect(url_for('homepage_customer'))



#search option
@app.route('/search',methods=['GET','POST'])
def search():
	data=request.form['data']
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM search")
	cur.execute("SELECT username FROM managers WHERE place='Accra'")
	var_username_Accra=cur.fetchall()
	cur.execute("SELECT username FROM managers WHERE place='Kumasi'")
	var_username_Kumasi=cur.fetchall()
	cur.execute("SELECT username FROM managers WHERE place='Takoradi'")
	var_username_Takoradi=cur.fetchall()
	conn.commit()
	conn.close()

	conn=sqlite3.connect('Accra.db')
	cur=conn.cursor()
	for x in var_username_Accra:
		cur.execute("SELECT * FROM {} WHERE item LIKE ?".format(x[0]),('%'+data+'%',))
		var=cur.fetchall()
		if var:
			for y in var:
				conn_temp=sqlite3.connect('members.db')
				cur_temp=conn_temp.cursor()
				cur_temp.execute("INSERT INTO search(item,def,price,category,place,rest,dish_image,company) VALUES(?,?,?,?,?,?,?,?); ",(y[0],y[1],y[2],y[3],'Accra',x[0],y[4],y[6]))
				conn_temp.commit()
				conn_temp.close()	
	conn.close()

	conn=sqlite3.connect('Kumasi.db')
	cur=conn.cursor()
	for x in var_username_Kumasi:
		cur.execute("SELECT * FROM {} WHERE item LIKE ?".format(x[0]),('%'+data+'%',))
		var=cur.fetchall()
		if var:
			for y in var:
				conn_temp=sqlite3.connect('members.db')
				cur_temp=conn_temp.cursor()
				cur_temp.execute("INSERT INTO search(item,def,price,category,place,rest,dish_image,company) VALUES(?,?,?,?,?,?,?,?); ",(y[0],y[1],y[2],y[3],'Kumasi',x[0],y[4],y[6]))
				conn_temp.commit()
				conn_temp.close()	
	conn.close()

	conn=sqlite3.connect('Takoradi.db')
	cur=conn.cursor()
	for x in var_username_Takoradi:
		cur.execute("SELECT * FROM {} WHERE item LIKE ?".format(x[0]),('%'+data+'%',))
		var=cur.fetchall()
		if var:
			for y in var:
				conn_temp=sqlite3.connect('members.db')
				cur_temp=conn_temp.cursor()
				cur_temp.execute("INSERT INTO search(item,def,price,category,place,rest,dish_image,company) VALUES(?,?,?,?,?,?,?,?); ",(y[0],y[1],y[2],y[3],'Takoradi',x[0],y[4],y[6]))
				conn_temp.commit()
				conn_temp.close()	
	conn.close()

	return redirect(url_for('search_result',data=data))



@app.route("/search_report", methods=["GET", "POST"])
def search_report():
    # Check if user is logged in
    if 'username' not in session:
        return "Unauthorized access"

    # Get username from session
    username = session['username']
    
    # Initialize new_orders variable
    new_orders = 0
    
    if request.method == "POST":
        # Handle POST request
        try:
            # Establish database connection
            with sqlite3.connect('members.db') as conn:
                cur = conn.cursor()
                
                # Count new orders for the logged-in user
                status = 'new'  # Adjust status as per your database schema
                cur.execute("SELECT count(*) FROM orders WHERE status=? AND rest=?", (status, username))
                new_orders = cur.fetchone()[0]
                
                # Retrieve orders for the logged-in user and specified date
                date = request.form["date"]
                cur.execute("SELECT * FROM orders WHERE rest LIKE ? AND date LIKE ? AND approve='Approved'", (f'%{username}%', date))
                rows = cur.fetchall()
                
                # Calculate total amount of orders
                totalAmount = sum(row[3] for row in rows)  # Assuming 'total' is the 4th column (index 3)
        
        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
            return "Database error occurred"
        
        # Render sales report template with data
        return render_template("sales_report.html", var=rows, totalAmount=totalAmount, date=date, new_orders=new_orders)
    
    # Handle GET request (initial page load)
    return render_template("noreport.html", new_orders=new_orders)



#to access after search is completed
@app.route('/search_result/<data>')
def search_result(data):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	dict={}
	cur.execute("SELECT * FROM search")
	var=cur.fetchall()
	cur.execute("SELECT * FROM managers WHERE username LIKE ?",('%'+data+'%',))
	var_rest=cur.fetchall()	
	for rest in var_rest:
		cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
		count=cur.fetchone()
		cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
		total_stars=cur.fetchall()
		sum=0
		for x in total_stars:
			sum=sum+x[0]
		if(count[0]==0):
			sum=0
		else:		
			sum=sum/count[0]			
		dict[rest[0],rest[3]]=sum
	conn.close()

	return render_template('search_result.html',var=var,var_rest=var_rest,data=data,dict=dict)


#to access after search is completed
# @app.route('/search_result/<data>')
# def search_result(data):
# 	conn=sqlite3.connect('members.db')
# 	cur=conn.cursor()
# 	dict={}
# 	cur.execute("SELECT * FROM SEARCH")
# 	var=cur.fetchall()
# 	cur.execute("SELECT * FROM managers WHERE username LIKE ?",('%'+data+'%',))
# 	var_rest=cur.fetchall()	
# 	for rest in var_rest:
# 		cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
# 		count=cur.fetchone()
# 		cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
# 		total_stars=cur.fetchall()
# 		sum=0
# 		for x in total_stars:
# 			sum=sum+x[0]
# 		if(count[0]==0):
# 			sum=0
# 		else:		
# 			sum=sum/count[0]			
# 		dict[rest[0],rest[3]]=sum
# 	conn.close()

# 	return render_template('search_result.html',var=var,var_rest=var_rest,data=data,dict=dict)

#to access after search sort for dishes is selected
@app.route('/search_result_sort/<sort>/<data>')
def search_result_sort(sort,data):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	dict={}
	if(sort=="desc"):
		cur.execute("SELECT * FROM SEARCH ORDER BY price DESC")
		var=cur.fetchall()
	if(sort=="asc"):
		cur.execute("SELECT * FROM SEARCH ORDER BY price ")
		var=cur.fetchall()	
	if(sort=="AtoZ"):
		cur.execute("SELECT * FROM SEARCH ORDER BY item")
		var=cur.fetchall()
	if(sort=="ZtoA"):
		cur.execute("SELECT * FROM SEARCH ORDER BY item DESC")
		var=cur.fetchall()	
	cur.execute("SELECT * FROM managers WHERE username LIKE ?",('%'+data+'%',))
	var_rest=cur.fetchall()	
	for rest in var_rest:
		cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
		count=cur.fetchone()
		cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
		total_stars=cur.fetchall()
		sum=0
		for x in total_stars:
			sum=sum+x[0]
		if(count[0]==0):
			sum=0
		else:		
			sum=sum/count[0]			
		dict[rest[0],rest[3]]=sum
	conn.close()

	return render_template('search_result.html',var=var,var_rest=var_rest,data=data,dict=dict)



#to access when search sort for restaurants is selected
@app.route('/search_result_sort_rest/<sort>/<data>')
def search_result_sort_rest(sort,data):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	dict={}
	cur.execute("SELECT * FROM SEARCH")
	var=cur.fetchall()
	if(sort=="asc"):
			cur.execute("SELECT * FROM managers WHERE username LIKE ? ORDER BY username",('%'+data+'%',))
			var_rest=cur.fetchall()
			for rest in var_rest:
				cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
				count=cur.fetchone()
				cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
				total_stars=cur.fetchall()
				sum=0
				for x in total_stars:
					sum=sum+x[0]
				if(count[0]==0):
					sum=0
				else:		
					sum=sum/count[0]			
				dict[rest[0],rest[3]]=sum
	elif(sort=="desc"):
		cur.execute("SELECT * FROM managers WHERE username LIKE ? ORDER BY username DESC",('%'+data+'%',))
		var_rest=cur.fetchall()
		for rest in var_rest:
			cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
			count=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
			total_stars=cur.fetchall()
			sum=0
			for x in total_stars:
				sum=sum+x[0]
			if(count[0]==0):
				sum=0
			else:		
				sum=sum/count[0]			
			dict[rest[0],rest[3]]=sum
	elif(sort=="rating"):	
		cur.execute("SELECT * FROM managers WHERE username LIKE ?",('%'+data+'%',))
		var_rest=cur.fetchall()
		for rest in var_rest:
			cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
			count=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(rest[3],rest[0],))
			total_stars=cur.fetchall()
			sum=0
			for x in total_stars:
				sum=sum+x[0]
			if(count[0]==0):
				sum=0
			else:		
				sum=sum/count[0]			
			dict[rest[0],rest[3]]=sum
		#to arrange dictionery in reverse order	
		conn.close()
		ord_dict = collections.OrderedDict(sorted(dict.items(), key=lambda x: x[1], reverse=True))
		return render_template('search_result_rating.html',var=var,var_rest=var_rest,data=data,ord_dict=ord_dict)

	conn.close()	
	return render_template('search_result.html',var=var,var_rest=var_rest,data=data,dict=dict)




#to access when location is selected from homepage_customer
@app.route('/<place>')			
def location(place):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	dict={}
	#shows all tables
	cur.execute("SELECT COUNT(*) FROM managers WHERE place=?",(place,))
	var=cur.fetchone()
	#if database in nonempty
	if(var[0]>0):   #since no row_factory=Row , coloumn number is used
		cur.execute("SELECT * FROM managers WHERE place=?",(place,))
		var=cur.fetchall()

		for rest in var:
			cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,rest[0],))
			count=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,rest[0],))
			total_stars=cur.fetchall()
			sum=0
			for x in total_stars:
				sum=sum+x[0]
			if(count[0]==0):
				sum=0
			else:		
				sum=sum/count[0]	
			#single key dictionery is used because no 2 restaurants will have same name			
			dict[rest[0]]=sum

		conn.close()
		return render_template('restaurants.html',var=var,place=place,dict=dict)		
		#from restaurants.html , goes to /menu/<var>
	else:
		return render_template('norestaurants.html')


#to access when location sort is selected 
@app.route('/sort/<place>/<sort>')			
def sort_location(place,sort):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	dict={}
	#shows all tables
	cur.execute("SELECT COUNT(*) FROM managers WHERE place=?",(place,))
	var=cur.fetchone()
	#if database in nonempty
	if(var[0]>0):   #since no row_factory=Row , coloumn number is used
		if(sort=="asc"):
			cur.execute("SELECT * FROM managers WHERE place=? ORDER BY username",(place,))
			var=cur.fetchall()
			for rest in var:
				cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,rest[0],))
				count=cur.fetchone()
				cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,rest[0],))
				total_stars=cur.fetchall()
				sum=0
				for x in total_stars:
					sum=sum+x[0]
				if(count[0]==0):
					sum=0
				else:		
					sum=sum/count[0]			
				dict[rest[0]]=sum
		elif(sort=="desc"):
			cur.execute("SELECT * FROM managers WHERE place=? ORDER BY username DESC",(place,))
			var=cur.fetchall()
			for rest in var:
				cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,rest[0],))
				count=cur.fetchone()
				cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,rest[0],))
				total_stars=cur.fetchall()
				sum=0
				for x in total_stars:
					sum=sum+x[0]
				if(count[0]==0):
					sum=0
				else:		
					sum=sum/count[0]			
				dict[rest[0]]=sum
		elif(sort=="rating"):	
			cur.execute("SELECT * FROM managers WHERE place=? ORDER BY username DESC",(place,))
			var=cur.fetchall()
			for rest in var:
				cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,rest[0],))
				count=cur.fetchone()
				cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,rest[0],))
				total_stars=cur.fetchall()
				sum=0
				for x in total_stars:
					sum=sum+x[0]
				if(count[0]==0):
					sum=0
				else:		
					sum=sum/count[0]			
				dict[rest[0]]=sum	
			#to arrange dictionery in reverse order	
			conn.close()
			ord_dict = collections.OrderedDict(sorted(dict.items(), key=lambda x: x[1], reverse=True))
			return render_template('restaurants_sort_rating.html',var=var,place=place,ord_dict=ord_dict)

		conn.close()
		return render_template('restaurants.html',var=var,place=place,dict=dict)		
		#from restaurants.html , goes to /menu/<var>
	else:
		return render_template('norestaurants.html')


#to access different menus of restaurants
@app.route('/<place>/menu/<rest>')
def menu(place,rest):
	#checks which place is selected ie which database 
	if(place=='Accra'):
		conn=sqlite3.connect('Accra.db')
	elif(place=='Kumasi'):
		conn=sqlite3.connect('Kumasi.db')
	else:
		conn=sqlite3.connect('location.db')
	conn.row_factory = sqlite3.Row
	cur=conn.cursor()
	cur.execute("SELECT COUNT(*) FROM {}".format(rest))
	var=cur.fetchone()
	if(var['count(*)']>0):	#since row_factory=Row,col name is used
		cur.execute("SELECT * FROM {} ".format(rest)) 
		var_veg=cur.fetchall()
		cur.execute("SELECT * FROM {} WHERE category='non-veg'".format(rest)) 
		var_non_veg=cur.fetchall()
		cur.execute("SELECT * FROM {} WHERE category='others'".format(rest)) 
		var_others=cur.fetchall()
		conn.close()

		conn=sqlite3.connect('members.db')
		cur=conn.cursor()
		cur.execute("SELECT * FROM managers WHERE place=? AND username=?",(place,rest,))
		temp=cur.fetchone()
		cur.execute("SELECT stars FROM rating WHERE place=? AND rest=? AND username=?",(place,rest,session['username'],))
		var_stars=cur.fetchone()
		cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,rest,))
		count=cur.fetchone()
		cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,rest,))
		total_stars=cur.fetchall()
		sum=0
		for x in total_stars:
			sum=sum+x[0]
		if(count[0]==0):
			sum=0
		else:		
			sum=sum/count[0]
		conn.close()
		#<var> variables contains all items in table, each row is accessed and displayed by colname
		return render_template('menu.html',var_veg=var_veg,var_non_veg=var_non_veg,var_others=var_others,place=place,rest=rest,temp=temp,var_stars=var_stars,sum=sum)
		#from menu.html , goes to /quantity/<item>/<price>
	else:
		return render_template('nomenu.html',place=place)


#rating..
@app.route('/<place>/<rest>/rating/<stars>')		
def rating(place,rest,stars):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("INSERT INTO rating(place,rest,username,stars) VALUES(?,?,?,?) ",(place,rest,session['username'],stars,))
	cur.execute("UPDATE reviews SET rating=? WHERE place=? AND rest=? AND username=?",(stars,place,rest,session['username'],))
	conn.commit()
	conn.close()
	return redirect(url_for('menu',place=place,rest=rest))



#rating..when user wants to change rating
@app.route('/<place>/<rest>/rating_change/<stars>')
def rating_change(place,rest,stars):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("UPDATE rating SET stars=? WHERE place=? AND rest=? AND username=?",(stars,place,rest,session['username'],))
	cur.execute("UPDATE reviews SET rating=? WHERE place=? AND rest=? AND username=?",(stars,place,rest,session['username'],))
	conn.commit()
	conn.close()
	return redirect(url_for('menu',place=place,rest=rest))




#when sorting is selected from menu
@app.route('/<place>/menu/<rest>/<sort>')
def menu_sort(place,rest,sort):
	if(place=='Accra'):
		conn=sqlite3.connect('Accra.db')
	elif(place=='Kumasi'):
		conn=sqlite3.connect('Kumasi.db')
	else:
		conn=sqlite3.connect('location.db')
	conn.row_factory = sqlite3.Row
	cur=conn.cursor()
	if(sort=="nameasc"):
		cur.execute("SELECT COUNT(*) FROM {}".format(rest))
		var=cur.fetchone()

		if(var['count(*)']>0):	#since row_factory=Row,col name is used
			cur.execute("SELECT * FROM {} WHERE category='veg' ORDER BY item ASC".format(rest)) 
			var_veg=cur.fetchall()
			cur.execute("SELECT * FROM {} WHERE category='non-veg' ORDER BY item ASC".format(rest)) 
			var_non_veg=cur.fetchall()
			cur.execute("SELECT * FROM {} WHERE category='others' ORDER BY item ASC".format(rest)) 
			var_others=cur.fetchall()
			conn.close()

			conn=sqlite3.connect('members.db')
			cur=conn.cursor()
			cur.execute("SELECT * FROM managers WHERE place=? AND username=?",(place,rest,))
			temp=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=? AND username=?",(place,rest,session['username'],))
			var_stars=cur.fetchone()
			cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,rest,))
			count=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,rest,))
			total_stars=cur.fetchall()
			sum=0
			for x in total_stars:
				sum=sum+x[0]
			if(count[0]==0):
				sum=0
			else:		
				sum=sum/count[0]
			conn.close()
			#<var> variables contains all items in table, each row is accessed and displayed by colname
			return render_template('menu.html',var_veg=var_veg,var_non_veg=var_non_veg,var_others=var_others,place=place,rest=rest,temp=temp,var_stars=var_stars,sum=sum)
			#from menu.html , goes to /quantity/<item>/<price>
		else:
			return render_template('nomenu.html',place=place)	

	elif(sort=="namedes"):
		cur.execute("SELECT COUNT(*) FROM {}".format(rest))
		var=cur.fetchone()
		if(var['count(*)']>0):	#since row_factory=Row,col name is used
			cur.execute("SELECT * FROM {} WHERE category='veg' ORDER BY item DESC".format(rest)) 
			var_veg=cur.fetchall()
			cur.execute("SELECT * FROM {} WHERE category='non-veg' ORDER BY item DESC".format(rest)) 
			var_non_veg=cur.fetchall()
			cur.execute("SELECT * FROM {} WHERE category='others' ORDER BY item DESC".format(rest)) 
			var_others=cur.fetchall()
			conn.close()

			conn=sqlite3.connect('members.db')
			cur=conn.cursor()
			cur.execute("SELECT * FROM managers WHERE place=? AND username=?",(place,rest,))
			temp=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=? AND username=?",(place,rest,session['username'],))
			var_stars=cur.fetchone()
			cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,rest,))
			count=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,rest,))
			total_stars=cur.fetchall()
			sum=0
			for x in total_stars:
				sum=sum+x[0]
			if(count[0]==0):
				sum=0
			else:		
				sum=sum/count[0]
			conn.close()
			#<var> variables contains all items in table, each row is accessed and displayed by colname
			return render_template('menu.html',var_veg=var_veg,var_non_veg=var_non_veg,var_others=var_others,place=place,rest=rest,temp=temp,var_stars=var_stars,sum=sum)
			#from menu.html , goes to /quantity/<item>/<price>
		else:
			return render_template('nomenu.html',place=place)	

	elif(sort=="pricelh"):
		cur.execute("SELECT COUNT(*) FROM {}".format(rest))
		var=cur.fetchone()
		if(var['count(*)']>0):	#since row_factory=Row,col name is used
			cur.execute("SELECT * FROM {} WHERE category='veg' ORDER BY price".format(rest)) 
			var_veg=cur.fetchall()
			cur.execute("SELECT * FROM {} WHERE category='non-veg' ORDER BY price".format(rest)) 
			var_non_veg=cur.fetchall()
			cur.execute("SELECT * FROM {} WHERE category='others' ORDER BY price".format(rest)) 
			var_others=cur.fetchall()
			conn.close()

			conn=sqlite3.connect('members.db')
			cur=conn.cursor()
			cur.execute("SELECT * FROM managers WHERE place=? AND username=?",(place,rest,))
			temp=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=? AND username=?",(place,rest,session['username'],))
			var_stars=cur.fetchone()
			cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,rest,))
			count=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,rest,))
			total_stars=cur.fetchall()
			sum=0
			for x in total_stars:
				sum=sum+x[0]
			if(count[0]==0):
				sum=0
			else:		
				sum=sum/count[0]
			conn.close()
			#<var> variables contains all items in table, each row is accessed and displayed by colname
			return render_template('menu.html',var_veg=var_veg,var_non_veg=var_non_veg,var_others=var_others,place=place,rest=rest,temp=temp,var_stars=var_stars,sum=sum)
			#from menu.html , goes to /quantity/<item>/<price>
		else:
			return render_template('nomenu.html',place=place)	

	elif(sort=="pricehl"):
		cur.execute("SELECT COUNT(*) FROM {}".format(rest))
		var=cur.fetchone()
		if(var['count(*)']>0):	#since row_factory=Row,col name is used
			cur.execute("SELECT * FROM {} WHERE category='veg' ORDER BY price DESC".format(rest)) 
			var_veg=cur.fetchall()
			cur.execute("SELECT * FROM {} WHERE category='non-veg' ORDER BY price DESC".format(rest)) 
			var_non_veg=cur.fetchall()
			cur.execute("SELECT * FROM {} WHERE category='others' ORDER BY price DESC".format(rest)) 
			var_others=cur.fetchall()
			conn.close()

			conn=sqlite3.connect('members.db')
			cur=conn.cursor()
			cur.execute("SELECT * FROM managers WHERE place=? AND username=?",(place,rest,))
			temp=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=? AND username=?",(place,rest,session['username'],))
			var_stars=cur.fetchone()
			cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,rest,))
			count=cur.fetchone()
			cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,rest,))
			total_stars=cur.fetchall()
			sum=0
			for x in total_stars:
				sum=sum+x[0]
			if(count[0]==0):
				sum=0
			else:		
				sum=sum/count[0]
			conn.close()
			#<var> variables contains all items in table, each row is accessed and displayed by colname
			return render_template('menu.html',var_veg=var_veg,var_non_veg=var_non_veg,var_others=var_others,place=place,rest=rest,temp=temp,var_stars=var_stars,sum=sum)
			#from menu.html , goes to /quantity/<item>/<price>
		else:
			return render_template('nomenu.html',place=place)	







#to submit quantity of item selected	
@app.route('/quantity/<place>/<rest>/<item>/<price>/<dish_image>',methods=['GET','POST'])
def quantity(place,rest,item,price,dish_image):
	return render_template('quantity.html',item=item,price=price,place=place,rest=rest,dish_image=dish_image)
	#from quantity.html , goes to /postquantity/<item>/<price>



#to insert quantity in CART table
@app.route('/postquantity/<place>/<rest>/<item>/<price>/<dish_image>',methods=['GET','POST'])
def postquantity(place,rest,item,price,dish_image):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	qty=request.form['qty']
	var=int(price)*int(qty)
	cur.execute("INSERT INTO {}(item,price,qty,total,place,rest,dish_image) VALUES(?,?,?,?,?,?,?); ".format("_"+session['username']) ,(item,price,qty,var,place,rest,dish_image,))
	conn.commit()
	conn.close()
	return redirect(url_for('homepage_customer'))

@app.route("/add_quantity/<id>")
def add_quantity(id):
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()
    
    find_table = "_" + session["username"]
    
    # Check if the item exists in the user's table
    cur.execute("SELECT * FROM {} WHERE item=?".format(find_table), (id,))
    check = cur.fetchone()
    
    if check:
        # Update quantity for the item
        cur.execute("UPDATE {} SET qty = qty + 1 WHERE item = ?".format(find_table), (id,))
        
        # Update total price for the item based on the updated quantity
        cur.execute("UPDATE {} SET total = qty * price WHERE item = ?".format(find_table), (id,))
        
        conn.commit()
        conn.close()

    return redirect(url_for('cartshow'))



@app.route("/approve_order/<id>")
def approve_order(id):
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()
    
    # find_table = "_" + session["username"]
    
    # Check if the item exists in the user's table
    cur.execute("SELECT * FROM orders  WHERE id=?", (id,))
    check = cur.fetchone()
    
    if check:
        # Update quantity for the itemdisptach_order
        cur.execute("UPDATE orders SET approve = 'Approved' WHERE id = ?", (id,))
        
        # Update total price for the item based on the updated quantity
        # cur.execute("UPDATE {} SET total = qty * price WHERE item = ?".format(find_table), (id,))
        
        conn.commit()
        conn.close()

    return redirect(url_for('m_orders'))



@app.route("/dispatch_order/<id>")
def dispatch_order(id):
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()
    
    # find_table = "_" + session["username"]
    
    # Check if the item exists in the user's table
    cur.execute("SELECT * FROM orders  WHERE id=?", (id,))
    check = cur.fetchone()
    
    if check:
        # Update quantity for the itemdisptach_order
        cur.execute("UPDATE orders SET approve = 'Dispatched' WHERE id = ?", (id,))
        
        # Update total price for the item based on the updated quantity
        # cur.execute("UPDATE {} SET total = qty * price WHERE item = ?".format(find_table), (id,))
        
        conn.commit()
        conn.close()

    return redirect(url_for('m_orders'))



@app.route("/deliver_order/<id>")
def deliver_order(id):
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()
    
    # find_table = "_" + session["username"]
    
    # Check if the item exists in the user's table
    cur.execute("SELECT * FROM orders  WHERE id=?", (id,))
    check = cur.fetchone()
    
    if check:
        # Update quantity for the itemdisptach_order
        cur.execute("UPDATE orders SET approve = 'Delivered' WHERE id = ?", (id,))
        
        # Update total price for the item based on the updated quantity
        # cur.execute("UPDATE {} SET total = qty * price WHERE item = ?".format(find_table), (id,))
        
        conn.commit()
        conn.close()

    return redirect(url_for('m_orders'))

@app.route("/cancel_order/<id>")
def cancel_order(id):
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()
    
    # find_table = "_" + session["username"]
    
    # Check if the item exists in the user's table
    cur.execute("SELECT * FROM orders  WHERE id=?", (id,))
    check = cur.fetchone()
    
    if check:
        # Update quantity for the item
        cur.execute("UPDATE orders SET approve = 'Cancelled' WHERE id = ?", (id,))
        
        # Update total price for the item based on the updated quantity
        # cur.execute("UPDATE {} SET total = qty * price WHERE item = ?".format(find_table), (id,))
        
        conn.commit()
        conn.close()

    return redirect(url_for('m_orders'))





def connect_db():
    """Establish and return a connection to the SQLite database."""
    return sqlite3.connect('members.db')
@app.route("/reset_password", methods=["POST"])
def reset_password():
    """Reset the password for a user based on their username."""
    
    # Clear the session username
    session.pop("username", None)
    
    # Retrieve form data
    username = request.form.get('username')
    new_password = request.form.get('password')  # Assuming you get the new password from the form

    # Validate input
    if not username or not new_password:
        flash("Username and new password are required.")
        return redirect(url_for('homepage'))

    # Connect to the database
    conn = connect_db()
    cur = conn.cursor()

    # Update password in the managers table
    cur.execute("SELECT * FROM managers WHERE username=?", (username,))
    if cur.fetchone():
        cur.execute("UPDATE managers SET password=? WHERE username=?", (new_password, username))
        conn.commit()
        conn.close()
        flash("Password reset successfully.")
        return redirect(url_for('homepage'))

    # Update password in the customers table
    cur.execute("SELECT * FROM customers WHERE username=?", (username,))
    if cur.fetchone():
        cur.execute("UPDATE customers SET password=? WHERE username=?", (new_password, username))
        conn.commit()
        conn.close()
        flash("Password reset successfully.")
        return redirect(url_for('homepage'))

    # If username is not found in either table
    conn.close()
    flash("Username not found in the database.")
    return redirect(url_for('homepage'))


# Handle cases where the request method is not POST
@app.errorhandler(405)
def method_not_allowed(error):
    flash("Method not allowed.")
    return redirect(url_for('homepage'))





def connect_db():
    # Adjust the database path as needed
    return sqlite3.connect('members.db')

@app.route("/manager_logged_in", methods=['POST'])
def manager_logged_in():
    if request.method == 'POST':
        username = request.form.get('username')

        if  username=="admin11":
            # flash("Username is required")
            return redirect(url_for('admin'))
		
        # Connect to the database
        conn = connect_db()
        cur = conn.cursor()

        # Check for active promotions (if needed, you can use this later)
        cur.execute("SELECT * FROM promotion WHERE status='1'")
        promotions = cur.fetchall()

        # Check if the username exists in the managers table and get the place
        cur.execute("SELECT place FROM managers WHERE username=?", (username,))
        place = cur.fetchone()
        
        if place:
            place = place[0]  # Extract the place from the tuple
            session['username'] = username  # Store username in session
            conn.close()
            return redirect(url_for('manager_homepage', place=place))
        
        # If username is not found in managers table, check the customers table
        cur.execute("SELECT * FROM customers WHERE username=?", (username,))
        customer = cur.fetchone()

        if customer:
            session['username'] = username  # Store username in session
            conn.close()
            return render_template('homepage_customer.html',promotions=promotions)
        
        conn.close()
        flash("Username not found in the database")
        return redirect(url_for('homepage'))
		

    # Handle cases where the request method is not POST
    flash("Method not allowed")
    return redirect(url_for('homepage'))

#to check for table in place


@app.route("/approve_advert/<id>")
def approve_advert(id):
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()
    
    # find_table = "_" + session["username"]
    
    # Check if the item exists in the user's table
    cur.execute("SELECT * FROM promotion  WHERE id=?", (id,))
    check = cur.fetchone()
    
    if check:
        # Update quantity for the item
        cur.execute("UPDATE promotion SET status = '1' WHERE id = ?", (id,))
        
        # Update total price for the item based on the updated quantity
        # cur.execute("UPDATE {} SET total = qty * price WHERE item = ?".format(find_table), (id,))
        
        conn.commit()
        conn.close()

    return redirect(url_for('advert'))

@app.route("/cancel_advert/<id>")
def cancel_advert(id):
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()
    
    # find_table = "_" + session["username"]
    
    # Check if the item exists in the user's table
    cur.execute("SELECT * FROM promotion  WHERE id=?", (id,))
    check = cur.fetchone()
    
    if check:
        # Update quantity for the item
        cur.execute("UPDATE promotion SET status = '0' WHERE id = ?", (id,))
        
        # Update total price for the item based on the updated quantity
        # cur.execute("UPDATE {} SET total = qty * price WHERE item = ?".format(find_table), (id,))
        
        conn.commit()
        conn.close()

    return redirect(url_for('advert'))





@app.route("/cancel_order_customer/<id>")
def cancel_order_customer(id):
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()
    
    # find_table = "_" + session["username"]
    
    # Check if the item exists in the user's table
    cur.execute("SELECT * FROM orders  WHERE id=?", (id,))
    check = cur.fetchone()
    
    if check:
        # Update quantity for the item
        cur.execute("UPDATE orders SET approve = 'Cancelled' WHERE id = ?", (id,))
        
        # Update total price for the item based on the updated quantity
        # cur.execute("UPDATE {} SET total = qty * price WHERE item = ?".format(find_table), (id,))
        
        conn.commit()
        conn.close()

    return redirect(url_for('orders'))

@app.route("/remove_quantity/<id>")
def remove_quantity(id):
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()
    
    find_table = "_" + session["username"]
    
    # Check if the item exists in the user's table
    cur.execute("SELECT * FROM {} WHERE item=?".format(find_table), (id,))
    check = cur.fetchone()
    
    if check:
        # Update quantity for the item
        cur.execute("UPDATE {} SET qty = qty - 1 WHERE item = ?".format(find_table), (id,))
        
        # Update total price for the item based on the updated quantity
        cur.execute("UPDATE {} SET total = qty * price WHERE item = ?".format(find_table), (id,))
        
        conn.commit()
        conn.close()

    return redirect(url_for('cartshow'))


@app.route('/cartshow')
def cartshow():
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()
    
    try:
        # Fetch managers (assuming it's necessary for context)
        cur.execute("SELECT * FROM managers")
        var2 = cur.fetchall()

        # Check if there are items in the cart
        cur.execute("SELECT COUNT(*) FROM {}".format("_"+session['username']))
        var1 = cur.fetchone()
        
        if var1[0] > 0:
            # Fetch all items in the cart
            cur.execute("SELECT * FROM {}".format("_"+session['username']))
            var = cur.fetchall()
            
            conn.commit()
            
            # Render cart if there are items, otherwise render nocart.html
            if var:
                return render_template('cartshow.html', var=var, var2=var2)
            else:
                return render_template("nocart.html")
        
        else:
            return render_template("nocart.html")
    
    except Exception as e:
        print(f"Error in cartshow: {str(e)}")
        conn.rollback()
        return f"Error in cartshow: {str(e)}" # Render your custom error page or handle error accordingly
    
    finally:
        conn.close()

@app.route('/cartremove/<item>/<place>/<rest>/<qty>')
def cartremove(item,place,rest,qty):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT COUNT(*) FROM {}".format("_"+session['username']))
	var1=cur.fetchone()
	if(var1[0]>0):
		cur.execute("DELETE FROM {} WHERE item=? AND place=? AND qty=?".format("_"+session['username']),(item,place,qty,))
		conn.commit()
		conn.close()
		return redirect(url_for('cartshow'))
	else:
		return render_template("nocart.html")

#to display total and proceed to pay
@app.route('/cartpay')
def cartpay():
	return render_template('cartpay.html')
	#two options in cartpay, card and COD

#to access if card is selected as mode of payment
@app.route('/paycard')
def paycard():
	return render_template('paycard.html')
	#from paycard.html , goes to /cartclear



#clear items in cart

from flask import Flask, session, redirect, url_for
import sqlite3
from datetime import datetime

@app.route('/cartclear')
def cartclear():
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if user not logged in

    username = session['username']
    orders_table = f"_{username}_orders"
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M")

    try:
        with sqlite3.connect('members.db') as conn:
            cur = conn.cursor()

            # Backup cart items to user's orders history
            cur.execute(f"SELECT * FROM _{username}")
            cart_items = cur.fetchall()

            # Fetch the phone number of the user
            cur.execute("SELECT phone FROM managers WHERE username = ?", (username,))
            user = cur.fetchone()
            phone = user[0] if user else None

            for item in cart_items:
                # Move items to orders history
                cur.execute(f"""
                    INSERT INTO {orders_table} 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    (*item, current_date)
                )

                # Fetch contact details of the restaurant manager
                cur.execute("SELECT phone FROM managers WHERE name = ?", (item[5],))
                manager = cur.fetchone()
                contact = manager[0] if manager else None

                # Record the order in a global orders table
                cur.execute("""
                    INSERT INTO orders 
                    (item, price, qty, total, place, rest, dish_image, phone, date, status, approve, contact) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (item[0], item[1], item[2], item[3], item[4], item[5], item[6], phone, current_date, "new", "Pending", contact)
                )

                # Update the most ordered table
                cur.execute("""
                    SELECT * FROM most_ordered 
                    WHERE place = ? AND rest = ? AND item = ?""",
                    (item[4], item[5], item[0])
                )
                check = cur.fetchone()

                if check:
                    cur.execute("""
                        UPDATE most_ordered 
                        SET orders = orders + ? 
                        WHERE place = ? AND rest = ? AND item = ?""",
                        (item[2], item[4], item[5], item[0])
                    )
                else:
                    cur.execute("""
                        INSERT INTO most_ordered 
                        (place, rest, item, orders, dish_image, price) 
                        VALUES (?, ?, ?, ?, ?, ?)""",
                        (item[4], item[5], item[0], item[2], item[6], item[1])
                    )

            # Record confirmation response
            cur.execute("""
                INSERT INTO response 
                (username, type, message, sender) 
                VALUES (?, ?, ?, ?)""",
                (username, 'confirmation', 'Order confirmed', 'admin')
            )

            # Clear the user's cart
            cur.execute(f"DELETE FROM _{username}")

            # Commit the transaction
            conn.commit()

    except sqlite3.Error as e:
        print(f"SQLite error in cartclear: {e}")
    
    return redirect(url_for('orders'))



#when user wants to see past orders
@app.route('/orders')
def orders():
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()
    temp = "_" + session['username'] + '_orders'
    cur.execute("SELECT * FROM orders WHERE	phone=? ORDER BY date DESC", (session['username'],))
    var = cur.fetchall()
    conn.close()
    
    if var:
        return render_template('orders.html', var=var)
    else:
        return render_template('no_orders.html')


@app.route('/m_orders')
def m_orders():
    status = 'new'
    conn = sqlite3.connect('members.db')
    cur = conn.cursor()
    cur.execute("UPDATE orders SET status = 'old' WHERE rest = ?", (session['username'],))
    conn.commit()
    # Retrieve orders for the current restaurant manager (assuming session['username'] is set)
    cur.execute("SELECT * FROM orders WHERE rest = ? ORDER BY date DESC", (session['username'],))
    var = cur.fetchall()
    
    # Count new orders for the current restaurant manager
    cur.execute("SELECT count(*) FROM orders WHERE status=? AND rest=?", (status, session['username']))
    new_orders = cur.fetchone()[0]
    
    conn.close()
    
    if var:
        return render_template('manager_order.html', var=var, new_orders=new_orders)
    else:
        return render_template('manager_order.html', var=var, new_orders=new_orders)




#for submitting feedback to manager from customer
@app.route('/feedback/<place>/<rest>',methods=['GET','POST'])
def feedback(place,rest):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	message=request.form['message']
	cur.execute("INSERT INTO feedback VALUES(?,?,?,?)",(place,rest,session['username'],message,))
	conn.commit()
	conn.close()
	return redirect(url_for('menu',place=place,rest=rest))



#to show reviews of restaurants
@app.route('/reviews/<place>/<rest>')
def reviews(place,rest):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM reviews WHERE place=? AND rest=?",(place,rest,))
	reviews=cur.fetchall()
	return render_template('reviews.html',place=place,rest=rest,reviews=reviews)


#to insert review in reviews table
@app.route('/review_post/<place>/<rest>',methods=['GET','POST'])
def review_post(place,rest):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	review=request.form['review']
	date=time.strftime("%x")
	cur.execute("SELECT stars FROM rating WHERE place=? AND rest=? AND username=?",(place,rest,session['username'],))
	stars=cur.fetchone()
	#if user has not rated the restaurant
	if not stars:
		cur.execute("INSERT INTO reviews(username,rest,place,date,rating,review) VALUES(?,?,?,?,?,?)",(session['username'],rest,place,date,0,review,))
	else:		
		cur.execute("INSERT INTO reviews(username,rest,place,date,rating,review) VALUES(?,?,?,?,?,?)",(session['username'],rest,place,date,stars[0],review,))
	conn.commit()
	conn.close()
	return redirect(url_for('reviews',place=place,rest=rest))

















#to access when manager_login is selected from homepage
@app.route('/manager_login',methods=['GET','POST'])
def manager_login():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM managers")
	var=cur.fetchall()
	conn.close()
	return render_template('manager_login.html',var=var)
	#from manager_login.html , if valid username , goes to /manager_logged_in	

#to access for new manager 
@app.route('/manager_signup')
def manager_signup():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT username,place FROM managers")
	var=cur.fetchall()
	cur.execute("SELECT username,place FROM approval")
	approval=cur.fetchall()
	conn.close()
	return render_template('manager_signup.html',var=var,approval=approval)


app.config['UPLOAD_FOLDER_REST']='static/restaurants/'
#when manager submites sign up form
@app.route('/manager_signed_up',methods=['GET','POST'])
def manager_signed_up():
	upload='static/restaurants/'
	place=request.form['place']
	username=request.form['username']
	password=request.form['password']
	location=request.form['location']
	phone=request.form['phone']
	start_time=request.form['start_time']
	close_time=request.form['close_time']
	email = request.form["email"]
	name = request.form["restaurant_name"]
	roles="manager"

	#The image file of restarant is received here
	file = request.files['filename']
	filename = secure_filename(file.filename)
	#The image is stored in static folder
	file.save(os.path.join(app.config['UPLOAD_FOLDER_REST'],filename))
	#renaming image file
	source=upload+filename
	destination=upload+place+'_'+username+'.jpg'
	os.rename(source,destination)


	#to create entry in approval table 
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("INSERT INTO approval(username,password,filename,place,location,phone,start,stop,email,role,name) values(?,?,?,?,?,?,?,?,?,?,?)",(username,password,place+'_'+username+'.jpg',place,location,phone,start_time,close_time,email,roles,name))
	conn.commit()
	conn.close()
	return render_template('manager_processing.html')


#when manager wants to logout
@app.route('/manager_logout')
def manager_logout():
    """Log out the manager by clearing the session and redirect to the homepage."""
    
    # Remove 'username' from the session to log out
    session.pop('username', None)
    
    # Redirect to the homepage
    return redirect(url_for('homepage'))



@app.route("/forget_password")
def forget_password():
	session.pop("username", None)
	return render_template("forget.html")



#manager session created after manager login
 # Make sure to set a secret key for session management


#to check for table in place
@app.route('/manager_homepage/<place>',methods=['GET','POST'])
def manager_homepage(place):
	if(place=='Accra'):
		conn=sqlite3.connect('Accra.db')
	elif(place=='Kumasi'):
		conn=sqlite3.connect('Kumasi.db')
	else:
		conn=sqlite3.connect('location.db')	
	cur=conn.cursor()
	username=session['username']
	#to select all table names in database
	cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
	var=cur.fetchall()
	conn.close()
	return redirect(url_for('manager_menu',place=place,username=username))
	

@app.route('/go_manager')
def go_manager():
    username = session.get("username")
    if username is None:
        # Handle the case where the username is not in the session
        return redirect(url_for('login'))  # Assuming you have a login route

    conn = sqlite3.connect('members.db')
    cur = conn.cursor()
    cur.execute("SELECT place FROM managers WHERE username=?", (username,))
    place_row = cur.fetchone()
    conn.close()
    
    if place_row is None:
        # Handle the case where no place is found for the username
        return redirect(url_for('error_page'))  # Assuming you have an error page route

    place = place_row[0]
    
    return redirect(url_for('manager_homepage', place=place))

        

        
	
#shows manager's menu
@app.route('/manager_menu/<place>/<username>')
def manager_menu(place,username):
	status ="new"
	if(place=='Accra'):
		conn=sqlite3.connect('Accra.db')
	elif(place=='Kumasi'):
		conn=sqlite3.connect('Kumasi.db')
	else:
		conn=sqlite3.connect('location.db')	
	cur=conn.cursor()
	cur.execute("SELECT * FROM {}".format(username))	#username is table name
	var=cur.fetchall()
	conn.close()
  
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM notification WHERE place=? AND rest=?",(place,username,))
	notification=cur.fetchall()
	cur.execute("SELECT * FROM feedback WHERE place=? AND rest=?",(place,username,))
	feedbacks=cur.fetchall()
	cur.execute("SELECT * FROM managers WHERE username=? AND place=?",(username,place,))	
	var1=cur.fetchone()
	cur.execute("SELECT stars FROM rating WHERE place=? AND rest=?",(place,username,))
	total_stars=cur.fetchall()
	cur.execute("SELECT count(*) FROM rating WHERE place=? AND rest=?",(place,username,))
	count=cur.fetchone()
	cur.execute("SELECT count(*) FROM orders WHERE status=? AND rest=?",(status,username,))
	new_orders =cur.fetchone()[0]
	conn.close()
	sum=0
	for x in total_stars:
		sum=sum+x[0]
	if(count[0]==0):
		sum=0
	else:		
		sum=sum/count[0]
	return render_template('manager_menu.html',new_orders=new_orders,var=var,var1=var1,place=place,username=username,sum=sum,feedbacks=feedbacks,notification=notification)
	#from manager_menu.html , goes to manager_edit based on action choice





#when manager wants to edit restaurant details
@app.route('/manager_edit_restaurant_form/<place>/<username>/<loc>/<ph>/<st>/<ct>/<di>')
def manager_edit_restarant_form(place,username,loc,ph,st,ct,di):
	return render_template('manager_edit_restaurant_form.html',place=place,username=username,loc=loc,ph=ph,st=st,ct=ct,di=di)


app.config['UPLOAD_FOLDER_REST1']='static/restaurants/'
#when manager wants to edit restaurant details
@app.route('/manager_edit_restaurant/<place>/<username>',methods=['GET','POST'])
def manager_edit_restarant(place,username):
	location=request.form['location']
	phone=request.form['phone']
	start_time=request.form['start_time']
	close_time=request.form['close_time']
	upload='static/restaurants/'

	#The image file of restarant is received here
	file = request.files['filename']
	if file:
		filename = secure_filename(file.filename)
		#to remove existing image
		source=upload+place+'_'+username+'.jpg'
		os.remove(source)

		#The image is stored in static folder
		file.save(os.path.join(app.config['UPLOAD_FOLDER_REST1'],filename))
		#renaming image file
		source=upload+filename
		destination=upload+place+'_'+username+'.jpg'
		os.rename(source,destination)

	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("UPDATE managers SET location=?,phone=?,start=?,stop=?,filename=? WHERE place=? AND username=?".format(username),(location,phone,start_time,close_time,place+'_'+username+'.jpg',place,username,))
	conn.commit()
	conn.close()
	return redirect(url_for('manager_homepage',place=place))





#to access when manager wants to edit items for manager_menu display
@app.route('/manager_edit/<place>/<username>/<action>',methods=['GET','POST'])
def manager_edit(place,username,action):
	if(action=="add"):
		if(place=='Accra'):
			conn=sqlite3.connect('Accra.db')
		elif(place=='Kumasi'):
			conn=sqlite3.connect('Kumasi.db')
		else:
			conn=sqlite3.connect('location.db')	
		cur=conn.cursor()
		cur.execute("SELECT item FROM {}".format(username))	
		var=cur.fetchall()
		conn.close()
		return render_template('manager_add.html',var=var,place=place,username=username)
	elif(action=="delete"):
		return redirect(url_for('manager_delete',place=place,username=username))
	elif(action=="editprice"):
		return redirect(url_for('manager_editprice',place=place,username=username))
	






app.config['UPLOAD_FOLDER_DISH'] = 'static/dish/'

#to access when manager wants to add items 
@app.route('/manager_add/<place>/<username>',methods=['GET','POST'])
def manager_add(place,username):
	conn =  sqlite3.connect('members.db')
	cur = conn.cursor()
	cur.execute("SELECT * FROM managers WHERE username=?", (username,))

	var=cur.fetchone()
	upload='static/dish/'
	item=request.form['item']
	def1=request.form['def'] 
	price=request.form['price']
	category=request.form['category']
	#The image file of dish is received here
	file = request.files['filename']
	filename = secure_filename(file.filename)
	#The image is stored in static folder
	file.save(os.path.join(app.config['UPLOAD_FOLDER_DISH'],filename))
	#renaming image file
	source=upload+filename
	destination=upload+place+'_'+username+'_'+item+'.jpg'
	os.rename(source,destination)

	if(place=='Accra'):
		conn=sqlite3.connect('Accra.db')
	elif(place=='Kumasi'):
		conn=sqlite3.connect('Kumasi.db')
	else:
		conn=sqlite3.connect('location.db')	
	cur=conn.cursor()
	cur.execute("INSERT INTO {}(item,def,price,category,dish_image,company) VALUES(?,?,?,?,?,?); ".format(username) ,(item,def1,price,category,place+'_'+username+'_'+item+'.jpg',var[10]))
	conn.commit()
	conn.close()
	return redirect(url_for('manager_menu',place=place,username=username))




#to access when manager wants to delete items 
@app.route('/manager_delete/<place>/<username>')
def manager_delete(place,username):
	if(place=='Accra'):
		conn=sqlite3.connect('Accra.db')
	elif(place=='Kumasi'):
		conn=sqlite3.connect('Kumasi.db')
	else:
		conn=sqlite3.connect('location.db')	
	cur=conn.cursor()
	cur.execute("SELECT COUNT(*) FROM {}".format(username))
	var1=cur.fetchone()
	#if table in nonempty
	if(var1[0]>0):
		cur.execute("SELECT * FROM {}".format(username))
		var=cur.fetchall()
		conn.close()
		return render_template('manager_delete.html',place=place,username=username,var=var)
	else:
		return render_template("no_managermenu.html",place=place,username=username)


#to delete items from database after manager selects delete items
@app.route('/manager_delete_database/<place>/<username>/<item>/<defen>')
def manager_delete_database(place,username,item,defen):
	if(place=='Accra'):
		conn=sqlite3.connect('Accra.db')
	elif(place=='Kumasi'):
		conn=sqlite3.connect('Kumasi.db')
	else:
		conn=sqlite3.connect('location.db')	
	cur=conn.cursor()
	upload='static/dish/'
	cur.execute("SELECT dish_image FROM {} WHERE item=? and def=?".format(username),(item,defen,))
	var=cur.fetchone()
	os.remove(upload+var[0])
	cur.execute("DELETE FROM {} WHERE item=? and def=?".format(username),(item,defen,))
	conn.commit()
	conn.close()

	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM most_ordered WHERE place=? AND rest=? AND item=?",(place,session['username'],item,))
	conn.commit()
	conn.close()
	return redirect(url_for('manager_menu',place=place,username=username))



#to access when manager wants to edit price of items 
@app.route('/manager_editprice/<place>/<username>')
def manager_editprice(place,username):
	if(place=='Accra'):
		conn=sqlite3.connect('Accra.db')
	elif(place=='Kumasi'):
		conn=sqlite3.connect('Kumasi.db')
	else:
		conn=sqlite3.connect('location.db')	
	cur=conn.cursor()
	cur.execute("SELECT COUNT(*) FROM {}".format(username))
	var1=cur.fetchone()
	#if table is nonempty
	if(var1[0]>0):
		cur.execute("SELECT * FROM {}".format(username))
		var=cur.fetchall()
		conn.close()
		return render_template('manager_editprice.html',place=place,username=username,var=var)
	else:
		return render_template("no_managermenu.html",place=place,username=username)



#to edit price of item from database after manager selects edit price
@app.route('/manager_editprice_newprice/<place>/<username>/<item>',methods=['GET','POST'])
def manager_editprice_newprice(place,username,item):
	return render_template('manager_editprice_newprice.html',place=place,username=username,item=item)



#to enter new price in manager_editprice_database
@app.route('/manager_editprice_database/<place>/<username>/<item>',methods=['GET','POST'])
def manager_editprice_database(place,username,item):
	if(place=='Accra'):
		conn=sqlite3.connect('Accra.db')
	elif(place=='Kumasi'):
		conn=sqlite3.connect('Kumasi.db')
	else:
		conn=sqlite3.connect('location.db')	
	cur=conn.cursor()
	price=request.form['price']
	cur.execute("UPDATE {} SET price=? WHERE item=?".format(username),(price,item,))
	conn.commit()
	conn.close()
	return redirect(url_for('manager_menu',place=place,username=username))



@app.route('/promote_shop',methods=['GET','POST'])
def promote_shop():
	username = session["username"]
	status="0"
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	fname=request.form['fname']
	lname = request.form["lname"]
	method = request.form["method"]
	amount=  request.form["amount"]
	company = request.form["company"]
	cur.execute("SELECT * FROM managers WHERE username=?", (username,))

	var=cur.fetchone()
	cur.execute("INSERT INTO promotion(fname,lastname,amount,method,username,status,filename,location,company) VALUES(?,?,?,?,?,?,?,?,?)",(fname,lname,amount,method,username,status,var[2],var[3],company,))
	conn.commit()
	conn.close()
	flash("Successful")
	return redirect(url_for('manager_menu',place=var[3],username=var[0]))	




#when manager wants to send response to customers
@app.route('/response_form_manager/<username>/<place>/<message>')
def response_form_manager(username,place,message):
	return render_template('response_form_manager.html',username=username,place=place,message=message)


#insert querys to response table
@app.route('/response_manager/<username>/<place>/<message>',methods=['GET','POST'])
def response_manager(username,place,message):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	response=request.form['message']
	cur.execute("DELETE FROM feedback WHERE username=? AND place=? AND rest=? AND message=?",(username,place,session['username'],message,))
	cur.execute("INSERT INTO response(username,message,sender) VALUES(?,?,?)",(username,response,session['username'],))
	conn.commit()
	conn.close()
	return redirect(url_for('manager_homepage',place=place))	


#when manager wants to remove feedbacks
@app.route('/remove_feedbacks/<place>/<username>')	
def remove_feedbacks(place,username):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM feedback WHERE place=? AND rest=?",(place,username,))
	conn.commit()
	conn.close()
	return redirect(url_for('manager_menu',place=place,username=username))


#when manager wants to remove notifications
@app.route('/remove_notifications/<place>/<username>')	
def remove_notifications(place,username):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM notification WHERE place=? AND rest=?",(place,username,))
	conn.commit()
	conn.close()
	return redirect(url_for('manager_menu',place=place,username=username))	

	

#to show reviews of restaurant
@app.route('/reviews_manager/<place>')
def reviews_manager(place):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM reviews WHERE place=? AND rest=?",(place,session['username'],))
	reviews=cur.fetchall()
	return render_template('reviews_manager.html',place=place,reviews=reviews)










@app.route("/advert")
def advert():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute('SELECT * FROM promotion')
	var=cur.fetchall()
	return render_template("advert.html",rows=var)




@app.route('/admin_access')
def admin_access():
	return render_template('admin_access.html')




@app.route('/admin')
def admin():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute('SELECT * FROM approval')
	var=cur.fetchall()
	cur.execute("SELECT username FROM customers")
	customers=cur.fetchall()
	cur.execute('SELECT * FROM managers WHERE place=?',('Accra',))
	var_Accra=cur.fetchall()
	cur.execute('SELECT * FROM managers WHERE place=?',('Kumasi',))
	var_Kumasi=cur.fetchall()
	cur.execute('SELECT * FROM managers WHERE place=?',('location',))
	var_location=cur.fetchall()
	cur.execute("SELECT * FROM messages")
	var_message=cur.fetchall()
	conn.close()
	return render_template('admin.html',var=var,var_Accra=var_Accra,var_Kumasi=var_Kumasi,var_location=var_location,var_message=var_message,customers=customers,)



#when admin wants to remove the request of new restaurant
@app.route('/admin_remove/<username>/<place>')
def admin_remove(username,place):
	upload='static/restaurants/'
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT filename FROM approval WHERE username=? AND place=?",(username,place,))
	var=cur.fetchone()
	#restaurant image is deleted 
	os.remove(upload+var[0])
	cur.execute('DELETE FROM approval WHERE username=? AND place=?',(username,place,))
	conn.commit()
	conn.close()
	return redirect(url_for('admin'))


#when admin wants to approve the request of new restaurant
@app.route('/admin_approve/<username>/<place>')
def admin_approve(username,place):
    # role="manager"
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()	
	cur.execute('SELECT * FROM approval WHERE username=? AND place=?',(username,place,))
	var=cur.fetchone()
 
	#to create entry in managers table 
	cur.execute("INSERT INTO managers(username,password,filename,place,location,phone,start,stop,email,role,name) values(?,?,?,?,?,?,?,?,?,?,?)",(var[0],var[1],var[2],var[3],var[4],var[5],var[6],var[7],var[8],var[9],var[10]))
	cur.execute("DELETE FROM approval WHERE username=? AND place=?",(username,place,))
	conn.commit()



	#to create username table in corresponding place database
	if(place=='Accra'):
		conn=sqlite3.connect('Accra.db')
	elif(place=='Kumasi'):
		conn=sqlite3.connect('Kumasi.db')
	else:
		conn=sqlite3.connect('location.db')	
	cur=conn.cursor()
	cur.execute("CREATE TABLE {}(item TEXT NOT NULL, def TEXT, price INTEGER NOT NULL, category TEXT, dish_image TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT,company TEXT)".format(username))

	conn.commit()
	conn.close()
	return redirect(url_for('admin'))



#when admin wants to remove message
@app.route("/admin_message_remove/<username>/<subject>")
def admin_message_remove(username,subject):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM messages WHERE username=? and subject=?",(username,subject,))
	conn.commit()
	conn.close()
	return redirect(url_for('admin'))


@app.route('/promote')
def promote():
	return render_template('promotion.html')

#when admin wants to send response to customers
@app.route('/response_form/<username>/<sub>')
def response_form(username,sub):
	return render_template('response_form.html',username=username,sub=sub)


#insert querys to response table
@app.route('/response/<username>/<sub>',methods=['GET','POST'])
def response(username,sub):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	message=request.form['message']
	cur.execute("DELETE FROM messages WHERE username=? AND subject=?",(username,sub,))
	cur.execute("INSERT INTO response(username,sub,message,sender) VALUES(?,?,?,?)",(username,sub,message,'admin',))
	conn.commit()
	conn.close()
	return redirect(url_for('admin'))	



#when admin wants to remove an existing restaurant	
@app.route('/admin_manage_remove/<username>/<place>')
def admin_manage_remove(username,place):
	upload='static/restaurants/'
	upload_dish='static/dish/'
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT filename FROM managers WHERE username=? AND place=?",(username,place,))
	var=cur.fetchone()
	
	#restaurant image is deleted 
	os.remove(upload+var[0])


	cur.execute('DELETE FROM managers WHERE username=? AND place=?',(username,place,))
	cur.execute("DELETE FROM rating WHERE place=? AND rest=?",(place,username,))
	cur.execute("DELETE FROM most_ordered WHERE place=? AND rest=?",(place,username,))
	conn.commit()
	conn.close()

	#to delete username table in corresponding place database
	if(place=='Accra'):
		conn=sqlite3.connect('Accra.db')
	elif(place=='Kumasi'):
		conn=sqlite3.connect('Kumasi.db')
	else:
		conn=sqlite3.connect('location.db')	
	cur=conn.cursor()
	cur.execute("SELECT * FROM {}".format(username))
	var=cur.fetchall()
	for x in var:
		os.remove(upload_dish+x[4])
	cur.execute("DROP TABLE {}".format(username))
	conn.commit()
	conn.close()
	return redirect(url_for('admin'))



#when admin wants to send notification to managers
@app.route('/notification_form/<rest>/<place>')
def notification_form(rest,place):
	return render_template('notification_form.html',rest=rest,place=place)


#insert querys to notification table
@app.route('/notification/<place>/<rest>',methods=['GET','POST'])
def notification(place,rest):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	message=request.form['message']
	cur.execute("INSERT INTO notification VALUES(?,?,?)",(place,rest,message,))
	conn.commit()
	conn.close()
	return redirect(url_for('admin'))


#to show restaurants table for reviews
@app.route('/admin_review')
def admin_review():
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT rest,place FROM reviews GROUP BY rest,place")
	var=cur.fetchall()
	conn.close()
	return render_template('admin_review.html',var=var)


#to show reviews of selected restaurant
@app.route('/admin_review_show/<place>/<rest>')
def admin_review_show(place,rest):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("SELECT * FROM reviews WHERE place=? AND rest=?",(place,rest,))
	reviews=cur.fetchall()
	return render_template('admin_review_show.html',reviews=reviews,place=place,rest=rest)


#when admin wants to remove a review
@app.route('/admin_review_remove/<place>/<rest>/<id_>')
def admin_review_remove(place,rest,id_):
	conn=sqlite3.connect('members.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM reviews WHERE id=?",(id_,))
	conn.commit()
	conn.close()
	return redirect(url_for('admin_review_show',place=place,rest=rest))


if __name__ == '__main__':
   init_db()
   app.run(debug = True)	

