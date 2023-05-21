import os
from datetime import datetime

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
connection = sqlite3.connect('finance.db')
db = connection.cursor()


from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
session(app)




# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    return apology("TODO")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method=="GET":
        return render_template("buy.html")
    else:
        if lookup(request.form.get("symbol")):
            id=str(session['user_id'])
            symbol=request.form.get("symbol").upper()
            username=db.execute("SELECT username FROM users WHERE id=?",id)[0]['username']
            price=lookup(request.form.get("symbol"))['price']
            shares=int(request.form.get("shares"))
            cost=shares*price
            name=lookup(symbol)['name']
            cash=db.execute("SELECT cash FROM users where id=?",id)[0]['cash']

            if (cash<cost):
                return apology("Not enough cash")
            else:
                print()
                #db.execute("UPDATE users SET cash=? where id=?",(cash-cost),id)
            count=int()
            count=db.execute(f"SELECT symbol  FROM {username} WHERE symbol = ?",symbol)
            userHistory=username+"History"
            db.execute(f"INSERT INTO  {userHistory} (symbol,shares,price,Transacted) VALUES(?,?,?,?)",symbol,shares,cost,datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            if len(count)>0:
                #symbol already in db that means the user already bbaught share for this
                shares=shares+db.execute(f"SELECT shares  FROM {username} WHERE symbol = ?",symbol)[0]['shares']
                cost=cost+db.execute(f"SELECT total  FROM {username} WHERE symbol = ?",symbol)[0]['total']
                db.execute(f"UPDATE {username} SET shares=?, price=?, total=? WHERE symbol=?",shares,price,cost,symbol)


            else:
                #insert the symbol in the table than call the function
                db.execute(f"INSERT INTO  {username} (symbol,name,shares,price,total) VALUES(?,?,?,?,?)",symbol,name,shares,price,cost)

            #will redirect to Bought! page after purchase
            purchase_history_dict=dict()
            purchase_history_dict=db.execute(f"SELECT * FROM {userHistory}" )
            return render_template("history.html",query=purchase_history_dict)













    return apology("TODO")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    id=str(session['user_id'])
    symbol=request.form.get("symbol").upper()
    userHistory=db.execute("SELECT username FROM users WHERE id=?",id)[0]['username']+"History"
    purchase_history_dict=dict()
    purchase_history_dict=db.execute(f"SELECT * FROM {userHistory}" )
    return render_template("history.html",query=purchase_history_dict)

    return apology("TODO")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 200)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 200)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 200)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/login")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method=="POST":
        query=lookup(request.form.get("symbol"))
        if query:
            return render_template("quote.html",query=query)
        else:
            return apology("INVALID SYMBOL")
    else:
        return render_template("quote.html")




@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
   # print(request.form.get("username"))
   # print(request.form.get("password"))
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        users=db.execute("SELECT username FROM users")

        # Ensure username was submitted
        if not username:
            return apology("must provide username", 400)


        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure passwords match
        elif not password == request.form.get("confirmation"):
            return apology("passwords must match", 400)

        else:
            for user in users:
                if user==username:
                    return apology("Username already taken!", 200)

            # Insert new user into database
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))
            db.execute(f"CREATE TABLE {username}(symbol varchar(255), name varchar(255),shares int,price float,total float)")
            username=username+"History"
            db.execute(f"CREATE TABLE {username}(symbol varchar(255),shares int,price float, Transacted varchar(255))")





            # Redirect user to home page
            return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")





@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    return apology("TODO")
#export API_KEY=pk_e4c617f3623d4edcb39b0e73e0fb0c8a

'''
username = a
password= ss

table for user  exists but there is extra '' while accessing from buy method.. neeed to find out the reason
solve= need to do f string where all the tabel name is a variable
'''