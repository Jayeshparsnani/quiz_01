import os, io
from flask import Flask,render_template,request, flash, redirect, url_for
import csv
import sqlite3
import base64
# from flask.ext.uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yxhtcfjgvkhbj#xhcf'  
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_content_length'] = 16*1024*1024

connection = sqlite3.connect('newdb.db')
try:
    connection.execute('CREATE TABLE if not exists people(Name varchar, Income varchar, Class varchar,Picture Text, Comments varchar)')
    print('Table created successfully')
except:
    print("Table not created")
finally:
    connection.close()


@app.route('/insertdata', methods=['POST'])
def insert_data():
    f = request.files['data_file']
    if not f:
        return "No file"
    # print(f)
    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    csv_input = csv.reader(stream)
    next(csv_input)
    # print("ino",csv_input)
    for row in csv_input:
        print(row)
        try:
            # print("here1")
            with sqlite3.connect("newdb.db") as con:
                # print("here2")
                cur = con.cursor()
                print(cur)
                cur.execute("INSERT INTO people(Name,Income,Class,Picture,Comments) VALUES (?,?,?,?,?)", (row[0],row[1],row[2],row[3],row[4]))
                print(1)
                con.commit()
                msg = "Record successfully added"
                print (msg)
            msg="Records inserted successfully"
        except:
            con.rollback()
            msg = "Error in insert operation"

        finally:
            con.close()
    flash(msg, 'error')
    return redirect(url_for('home'))

@app.route('/getrecords', methods=['POST'])
def get_records():
    con = sqlite3.connect("newdb.db")
    cur = con.cursor()
    cur.execute("select * from people")
    con.commit()
    rows = cur.fetchall();
    if not rows:
        flash('Table is empty', 'error')
        return redirect(url_for('home'))
    # print(rows)
    con.close()
    return render_template("result_page.html", msg=rows, unique = "displayrecords")

@app.route('/searchname', methods=['POST'])
def search_name():
    name=request.form['name']
    # print(name)
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("select * from people where Name=?",(name,))
    con.commit()
    rows = cur.fetchall();
    if not rows:
        flash('No such record found', 'error')
        return redirect(url_for('home'))
    print(rows)
    con.close()
    return render_template("result_page.html", msg=rows, unique = "displayname")

@app.route('/addpicture', methods=['POST'])
def add_picture():
    name=request.form['name']
    pic = request.files['image']
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    # cur.execute("select Picture from people where Name=?",(name,))
    # con.commit()
    # rows = list(cur.fetchall());
    # print(rows)
    if not name == "":
        encoded_string = base64.b64encode(pic.read())
        # print(encoded_string)
        ds = encoded_string.decode('utf_8')
        # print(ds)
        cursor = con.cursor()
        cursor.execute('UPDATE people SET Picture = ? where Name = ?', (ds,name))
        rows = cursor.fetchall()
        print(rows)
    print(rows)
    return render_template("result_page.html", image=rows, unique = "displayimg")

@app.route('/nameimage', methods=['POST'])
def nameimage():
    con = sqlite3.connect("newdb.db")
    cur = con.cursor()
    cur.execute("select * from people")
    con.commit()
    rows = cur.fetchall();
    print(rows)
    if not rows:
        flash('Errorr', 'error')
        return redirect(url_for('home'))
    con.close()
    return render_template("result_page.html", msg=rows, unique = "nameimagepic")

@app.route('/changecomment', methods=['POST'])
def change_keyword():
    name = request.form['name']
    comment = request.form['comment']
    income = request.form['income']
    print(name)
    con = sqlite3.connect("newdb.db")
    cur = con.cursor()
    cur.execute("select * from people where Name=?",(name,))
    rows = cur.fetchall()
    if not rows:
        flash('No user found', 'error')
        return redirect(url_for('home'))
    cur.execute("UPDATE people SET Comments = ?, Income=? WHERE Name =?", (comment,income,name))
    con.commit()
    con.close()
    flash('User Comment changed Succesfully', 'Success')
    return redirect(url_for('home'))
    


@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

