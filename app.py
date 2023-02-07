import os, io
from flask import Flask,render_template,request, flash, redirect, url_for
import csv
import sqlite3
import base64
# from flask.ext.uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
app.config['SECRET_KEY'] = 'twrxhcfjgvh3456#xhcf'  
app.config['UPLOAD_FOLDER'] = 'static/images'
app.config['MAX_content_length'] = 16*1024*1024

connection = sqlite3.connect('database.db')
try:
    connection.execute('CREATE TABLE if not exists people(Name varchar, State varchar, Salary varchar,Grade varchar, Room varchar,TelNum varchar, Picture Text, Keywords varchar)')
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
            with sqlite3.connect("database.db") as con:
                # print("here2")
                cur = con.cursor()
                print(cur)
                cur.execute("INSERT INTO people(Name,State,Salary,Grade,Room,TelNum,Picture,Keywords) VALUES (?,?,?,?,?,?,?,?)", (row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7]))
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
    con = sqlite3.connect("database.db")
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

@app.route('/getImgRecLess90000', methods=['POST'])
def getImgRecLess90000():
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("select * from people where Salary<99000")
    con.commit()
    rows = cur.fetchall();
    if not rows:
        flash('No such record found whose salary is less than 99000', 'error')
        return redirect(url_for('home'))
    con.close()
    return render_template("result_page.html", msg=rows, unique = "salary99000")

@app.route('/deleteuser', methods=['POST'])
def removeuser():
    name=request.form['delete_user']
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("delete from people where Name=?",(name,))
    con.commit()
    con.close()
    flash('User Deleted Succesfully', 'Success')
    return redirect(url_for('home'))

@app.route('/changekeyword', methods=['POST'])
def change_keyword():
    name = request.form['name']
    keyword = request.form['keyword']
    print(name)
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("select * from people where Name=?",(name,))
    rows = cur.fetchall()
    if not rows:
        flash('No user found', 'error')
        return redirect(url_for('home'))
    cur.execute("UPDATE people SET Keywords = ? WHERE Name =?", (keyword, name,))
    con.commit()
    con.close()
    flash('User keyword changed Succesfully', 'Success')
    return redirect(url_for('home'))
    

@app.route('/changesalary', methods=['POST'])
def change_salary():
    name = request.form['name']
    salary = request.form['salary']
    print(name)
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    cur.execute("select * from people where Name=?",(name,))
    rows = cur.fetchall()
    if not rows:
        flash('No user found', 'error')
        return redirect(url_for('home'))
    cur.execute("UPDATE people SET Salary = ? WHERE Name =?", (salary, name,))
    con.commit()
    con.close()
    flash('User Salary changed Succesfully', 'Success')
    return redirect(url_for('home'))


@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)


#References used:
# 1. To connect to database: https://www.digitalocean.com/community/tutorials/how-to-use-an-sqlite-database-in-a-flask-application
# 2. Insert image in blob file: https://stackoverflow.com/questions/14704559/how-to-insert-image-in-mysql-databasetable
# 3. To upload image: https://flask-uploads.readthedocs.io/en/latest/  ,https://medium.com/@dustindavignon/upload-multiple-images-with-python-flask-and-flask-dropzone-d5b821829b1d