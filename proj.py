import sqlite3 
from flask import Flask ,flash,session,render_template,redirect,escape, url_for,request


app = Flask(__name__)
app.secret_key = 'any random string'


@app.route('/')
def homepage():
	return render_template('homepage.html')


#to access when location is selected from homepage
@app.route('/<place>')			
def location(place):
	#checks which place is selected in homepage ie which databse
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')
	cur=conn.cursor()
	#shows all tables
	cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type = 'table'")
	var=cur.fetchone()
	#if database in nonempty
	if(var[0]>0):   #since no row_factory=Row , coloumn number is used
		cur.execute("SELECT name FROM sqlite_master WHERE type = 'table' ")
		var=cur.fetchall()
		conn.close()
		return render_template('restaurants.html',var=var,place=place)		
		#from restaurants.html , goes to /menu/<var>
	else:
		return render_template('norestaurants.html')



#to access different menus of restaurants
@app.route('/<place>/menu/<rest>')
def menu(place,rest):
	#checks which place is selected ie which database 
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')
	conn.row_factory = sqlite3.Row
	cur=conn.cursor()
	cur.execute("SELECT COUNT(*) FROM {}".format(rest))
	var=cur.fetchone()
	if(var['count(*)']>0):	#since row_factory=Row,col name is used
		cur.execute("SELECT * FROM {}".format(rest)) 
		var=cur.fetchall()
		conn.close()
		#<var> contains all items in table, each row is accessed and displayed by colname
		return render_template('menu.html',var=var,place=place,rest=rest)
		#from menu.html , goes to /quantity/<item>/<price>
	else:
		return render_template('nomenu.html',place=place)
	

#to submit quantity of item selected	
@app.route('/quantity/<place>/<rest>/<item>/<price>',methods=['GET','POST'])
def quantity(place,rest,item,price):
	return render_template('quantity.html',item=item,price=price,place=place,rest=rest)
	#from quantity.html , goes to /postquantity/<item>/<price>



#to insert quantity in CART table
@app.route('/postquantity/<place>/<rest>/<item>/<price>',methods=['GET','POST'])
def postquantity(place,rest,item,price):
	print('postquantity')
	conn=sqlite3.connect('bucket.db')
	cur=conn.cursor()
	qty=request.form['qty']
	var=int(price)*int(qty)
	cur.execute("INSERT INTO CART(item,price,qty,total,place,rest) VALUES(?,?,?,?,?,?); " ,(item,price,qty,var,place,rest))
	conn.commit()
	conn.close()
	return redirect(url_for('homepage'))









#to show items in cart
@app.route('/cartshow')
def cartshow():
	conn=sqlite3.connect('bucket.db')
	cur=conn.cursor()
	cur.execute("SELECT COUNT(*) FROM CART")
	var1=cur.fetchone()
	if(var1[0]>0):
		cur.execute("SELECT * FROM CART")
		var=cur.fetchall()
		conn.close()
		return render_template('cartshow.html',var=var)
		#from cartshow.html , goes to cartremove/<item> 
	else:
		return render_template("nocart.html")

#to delete an <item> from cart
@app.route('/cartremove/<item>/<place>/<rest>')
def cartremove(item,place,rest):
	conn=sqlite3.connect('bucket.db')
	cur=conn.cursor()
	cur.execute("SELECT COUNT(*) FROM CART")
	var1=cur.fetchone()
	if(var1[0]>0):
		cur.execute("DELETE FROM CART WHERE item=? AND place=?",(item,place))
		conn.commit()
		conn.close()
		return redirect(url_for('cartshow'))
	else:
		return render_template("nocart.html")

#to display total and proceed to pay
@app.route('/cartpay')
def cartpay():
	conn=sqlite3.connect('bucket.db')
	cur=conn.cursor()
	cur.execute("SELECT COUNT(*) FROM CART")
	var=cur.fetchone()
	nitem=var[0]
	cur.execute("SELECT SUM(total) FROM CART")
	var=cur.fetchone()
	ntotal=var[0]
	return render_template('cartpay.html',nitem=nitem,ntotal=ntotal)
	#two options in cartpay, card and COD

#to access if card is selected as mode of paymeny
@app.route('/paycard')
def paycard():
	return render_template('paycard.html')
	#from paycard.html , goes to /cartclear

#to access if COD is selected as mode of payment
@app.route('/paycash')
def paycash():
	return render_template('paycash.html')	
	#from paycash.html , goes to /cartclear

#clear items in cart
@app.route('/cartclear')
def cartclear():
	conn=sqlite3.connect('bucket.db')
	cur=conn.cursor()
	cur.execute("DELETE FROM CART")
	conn.commit()
	conn.close()
	return redirect(url_for('homepage'))
















#to access when login is selected from homepage
@app.route('/login',methods=['GET','POST']	)
def login():
	return render_template('login.html')
	#from login.html , if valid username , goes to /success	

#to check for table in place
@app.route('/success',methods=['GET','POST'])
def success():
	username=request.form['username']
	place=request.form['location']
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')	
	cur=conn.cursor()
	#to select all table names in database
	cur.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
	var=cur.fetchall()
	conn.close()
	for x in var:
		if(username==x[0]):
			#if username table is present in database
			return redirect(url_for('manager_menu',place=place,username=username))
			break
	return render_template('nomanager.html')

#shows manager's menu
@app.route('/manager_menu/<place>/<username>')
def manager_menu(place,username):
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')	
	cur=conn.cursor()
	cur.execute("SELECT * FROM {}".format(username))	#username is table name
	var=cur.fetchall()
	conn.close()
	return render_template('manager_menu.html',var=var,place=place,username=username)
	#from manager_menu.html , goes to manager_edit based on action choice
	


#to access when manager wants to edit items for manager_menu display
@app.route('/manager_edit/<place>/<username>/<action>',methods=['GET','POST'])
def manager_edit(place,username,action):
	if(action=="add"):
		return render_template('manager_add.html',place=place,username=username)
	elif(action=="delete"):
		print('success')
		return redirect(url_for('manager_delete',place=place,username=username))
	
	







#to access when manager wants to add items 
@app.route('/manager_add/<place>/<username>',methods=['GET','POST'])
def manager_add(place,username):
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')	
	cur=conn.cursor()
	item=request.form['item']
	def1=request.form['def'] 
	price=request.form['price']
	cur.execute("INSERT INTO {}(item,def,price) VALUES(?,?,?); ".format(username) ,(item,def1,price))
	conn.commit()
	conn.close()
	return redirect(url_for('manager_menu',place=place,username=username))








#to access when manager wants to delete items 
@app.route('/manager_delete/<place>/<username>')
def manager_delete(place,username):
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')	
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
@app.route('/manager_delete_database/<place>/<username>/<item>')
def manager_delete_database(place,username,item):
	if(place=='TLY'):
		conn=sqlite3.connect('TLY.db')
	elif(place=='KANNUR'):
		conn=sqlite3.connect('KANNUR.db')
	else:
		conn=sqlite3.connect('CALICUT.db')	
	cur=conn.cursor()
	cur.execute("DELETE FROM {} WHERE item=?".format(username),(item,))
	conn.commit()
	return redirect(url_for('manager_menu',place=place,username=username))









@app.route('/login1')
def login1():
	return render_template('login1.html')








if __name__ == '__main__':
   app.run(debug = True)	

