from flask import Flask, render_template, request, flash, redirect, url_for
import pyodbc

app = Flask(__name__)

app.config['SECRET_KEY'] = 'wzdxhfgvhjb87654exfgu876'


server = 'tcp:jayeshparsnani1234.database.windows.net' 
database = 'JayeshParsnani' 
username = 'JayeshParsnani8805' 
password = 'Password@1234' 
cnxn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password,autocommit=True)
cursor = cnxn.cursor()



@app.route('/getrecords', methods=['POST'])
def get_records():
    cursor.execute("select * from people")
    rows = cursor.fetchall()
    if not rows:
        flash('Table is empty', 'error')
        return redirect(url_for('index'))
    # print(rows)
    # con.close()
    return render_template("result_page.html", msg=rows, unique = "displayrecords")

@app.route('/nameimage', methods=['POST'])
def nameimage():
    cursor.execute("select * from people")
    cursor.commit()
    rows = cursor.fetchall()
    print(rows)
    if not rows:
        flash('Errorr', 'error')
        return redirect(url_for('index'))
    # cursor.close()
    return render_template("result_page.html", msg=rows, unique = "nameimagepic")

@app.route('/changecomment', methods=['POST'])
def change_keyword():
    name = request.form['name']
    comment = request.form['comment']
    income = request.form['income']
    print(name)
    cursor.execute("select * from people where Name=?",(name,))
    rows = cursor.fetchall()
    if not rows:
        flash('No user found', 'error')
        return redirect(url_for('index'))
    cursor.execute("UPDATE people SET Comments = ?, Income=? WHERE Name =?", (comment,income,name))
    cursor.commit()

    flash('User Comment changed Succesfully', 'Success')
    return redirect(url_for('index'))
    


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

