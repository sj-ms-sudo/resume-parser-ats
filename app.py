import PyPDF2
from flask import Flask,request,render_template,redirect,session,url_for,g
import spacy
import re
from werkzeug.security import check_password_hash
import sqlite3
import json
nlp = spacy.load("en_core_web_md")
skill = []
skills=[]
name =None
email = None
phone = None
app = Flask(__name__)
app.secret_key='supersecret'
@app.route("/visuals")
def visuals():
    db = sqlite3.connect('resume.db')
    cursor = db.cursor()
    cursor.execute("SELECT name, ats FROM resume ORDER BY ats DESC")
    data = cursor.fetchall()
    db.close()
    return render_template("visuals.html", data=json.dumps(data))
@app.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username = ?",(username,))
        us = c.fetchone()
        conn.close()
        if us and check_password_hash(us[0],password):
            session["user"] = username
            return redirect(url_for('admin'))
        else:
            return "Invalid Credentials"
    return render_template("login.html")
@app.route("/admin")
def admin():
    if "user" in session:
        return render_template("admin.html")
    else:
        return "Not authorized"
@app.route("/admindash", methods=["GET", "POST"])
def admindash():
    db = sqlite3.connect('resume.db')
    cursor = db.cursor()
    if request.method == "POST":
        if "clear" in request.form:
            cursor.execute("DELETE FROM resume")
            db.commit() 
    cursor.execute("SELECT * FROM resume ORDER BY ats DESC")
    commit = cursor.fetchall()

    db.close()
    return render_template("admindash.html", commit=commit)
@app.route("/addskill",methods=["GET","POST"])
def addskill():
    if "user" in session:
        newskills=""
        if request.method =="POST":
            if "add" in request.form:
                conn=sqlite3.connect('skills.db')
                c = conn.cursor()
                sk = request.form["skills"]
                skills = [s.strip().lower() for s in sk.split(',')]
                for ski in skills:
                    c.execute("INSERT INTO skills(Skills)VALUES(?)",(ski,))
                conn.commit()
                conn.close()
            if "clear" in request.form:
                conn=sqlite3.connect('skills.db')
                c=conn.cursor()
                c.execute("DELETE FROM skills")
                conn.commit()
                conn.close()
        return render_template("addskill.html")
    else:
        return "Not authorized"
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/resume")
def resume():
    return render_template("resume.html")
@app.route("/dashboard",methods=["POST"])
def dashboard():
    file = request.files["file"]
    try:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text+=page.extract_text()
        doc =nlp(text)
        for ent in doc.ents:
            if ent.label_ =="PERSON":
                name = ent.text
                break
        e = re.search(r"[a-zA-Z0-9]+@[a-zA-Z0-9]+.[a-z]{2,}",doc.text)
        if e:
            email = e.group()
        p = re.search(r"\+\d{2,3}\s\d{7,12}",doc.text)
        if p:
            phone = p.group()
        conn  =sqlite3.connect('skills.db')
        c = conn.cursor()
        c.execute("SELECT * FROM skills")
        rows = c.fetchall()
        skills = [row[0] for row in rows]
        conn.close()
        for token in doc:
            if token.text.lower() in skills and token.text not in skill:
                skill.append(token.text)
        ats = (len(skill)/len(skills))*100
        id = {"Name":name,"Email":email,"Phone":phone,"Skills":skill,"ats":ats}
        conn = sqlite3.connect('resume.db')
        c = conn.cursor()
        c.execute("INSERT INTO resume (name,email,phone,skills,ats) VALUES(?,?,?,?,?)",(name,email,phone,json.dumps(skill),ats))
        conn.commit()
        conn.close()
    except Exception as e:
        return f"Error {e}",400
    return render_template("dashboard.html",id=id)
if __name__ =="__main__":
    app.run(debug=True)