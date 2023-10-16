from flask import Flask, render_template, request, redirect
import sqlite3 as sql
app = Flask(__name__)
conn = sql.connect('database.db')
conn.execute('CREATE TABLE  IF NOT EXISTS PRODUCTS (ID INTEGER PRIMARY KEY AUTOINCREMENT,PRONAME TEXT,PRICE NUMERIC);');
conn.close()
@app.route('/',methods=['POST',"GET"])
def index():
    if request.method == "POST":
        proname = request.form["proname"]
        proprice = request.form["proprice"]
        prostock = request.form["lst"]
        con = sql.connect("database.db")
        cur = con.cursor()
        cur.execute("INSERT INTO PRODUCTS (ID,PRONAME,PRICE) VALUES (NULL,?,?)", (proname,proprice))
        con.commit()
    return render_template("index.html")
@app.route('/show')
def showall():
    con = sql.connect("database.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("select * from products")
    rows = cur.fetchall();
    return render_template("show.html",rows = rows)
@app.route('/edit/<int:id>')
def edit(id):
    con = sql.connect("database.db")
    cur = con.cursor()
    cur.execute(f"select * from products WHERE ID = {id}")
    rows = cur.fetchall();
    return render_template("edit.html", rows=rows)
@app.route('/update',methods=['POST'])
def update():
    proname = request.form["proname"]
    proprice = float(request.form["proprice"])
    id =  request.form['txtid']
    con = sql.connect("database.db")
    cur = con.cursor()
    query = f"UPDATE PRODUCTS SET PRONAME = '{proname}', PRICE = {proprice} WHERE ID ={id}";
    print(query)
    cur.execute(query)
    con.commit()
    return redirect('/show')
@app.route('/delete/<int:id>')
def delete(id):
    con = sql.connect("database.db")
    cur = con.cursor()
    query = f"DELETE FROM PRODUCTS WHERE ID ={id}";
    print(query)
    cur.execute(query)
    con.commit()
    return redirect('/show')