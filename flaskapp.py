from flask import Flask, render_template, redirect, url_for, request
import sqlite3
app = Flask(__name__)


conn = sqlite3.connect('database.db')
print("connected Database")
cur = conn.cursor()
try:
    cur.execute("SELECT 1 FROM students LIMIT 1;")
    conn.close()
except: 
    conn.execute('CREATE TABLE students(name TEXT NOT NULL, email TEXT PRIMARY KEY, city TEXT, pin TEXT )')
    print("Table created successfully")
    conn.close()

@app.route('/')
def home():
   return render_template('hello.html')

@app.route('/enternew')
def new_student():
    return  render_template('student.html')

@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            email = request.form['email']
            city = request.form['city']
            pin = request.form['pin']

            con = sqlite3.connect('database.db') 
            cur = con.cursor()
            cur.execute("INSERT INTO students (name,email,city,pin) VALUES (?,?,?,?)",(nm,email,city,pin) )
            con.commit()
            msg = "Record successfully added"

        except:
            con.rollback()
            msg = "Record not inserted- Check if the record already exists; If not enter your details correctly"
        
        finally:
            return render_template("result.html",msg = msg)
            con.close()

@app.route('/list')
def list():
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row

    cur = con.cursor()
    cur.execute("select * from students")    

    rows = cur.fetchall()
    return render_template("list.html", rows= rows)

if __name__ == '__main__':
    app.run(debug = True)
