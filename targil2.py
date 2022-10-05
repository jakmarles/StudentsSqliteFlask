import json
from flask import Flask,request

from enum import Enum
import sqlite3
conn = sqlite3.connect("my_contacts.db",check_same_thread=False)
cur = conn.cursor()
# cur.execute("CREATE TABLE Contacts(Contacts_id INTEGER PRIMARY KEY, Name char(30));")

conn.commit()

app = Flask(__name__)

my_data=[{"1":"idan"},{"2":"matan"},{"3":"or"}]
@app.route("/")
def home():
    return '<h1>please type your request in the URL'


@app.route("/data/<ind>")
@app.route("/data/")
def students(ind=-1):
    with conn:
        if int(ind) < 0:
            cur.execute("SELECT * FROM Contacts WHERE Name IS NOT NULL")
            return (cur.fetchall())
        else:
            cur.execute("""SELECT * FROM Contacts WHERE Contacts_id=?""", (ind,))
            return (cur.fetchall())
    

@app.route("/add/", methods=['POST'])
def add_student():
        # get the data from user
        data= request.json
        s_name = (data["name"])
        cur.execute("""INSERT INTO Contacts(Name)VALUES (?)""", (s_name,))
        conn.commit()
        print(f"added {s_name} to the contacts")
        return "student added"

@app.route("/del/<ind>", methods=['DELETE'])
def del_student(ind=-1):
    if int(ind) > -1:
        searchinput = ind
        cur.execute(f"Update Contacts set name = NULL WHERE Contacts_id = {searchinput}")
        conn.commit()
        print('Contact has been removed')
        return "student del"

@app.route("/upd/<ind>", methods=['PUT'])
def upd_student(ind=-1):
        if int(ind) > -1:
            data= request.json
            uname = (data["name"])
            searchinput = ind
            conn.execute(f"UPDATE Contacts SET Name ='{uname}' WHERE Contacts_id = {searchinput}")
            conn.commit()
            print('Contact has been Updated')
            return "student update"



app.run(debug=True)