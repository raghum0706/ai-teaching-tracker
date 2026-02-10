from flask import Blueprint, render_template, request, redirect, session
import sqlite3

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        cur.execute("SELECT id, role FROM users WHERE username=? AND password=?", (username, password))
        user = cur.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["role"] = user[1]
            return redirect("/dashboard")
        return "Invalid login details."
    
    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
