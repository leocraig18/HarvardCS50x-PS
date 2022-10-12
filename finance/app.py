import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
import math

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

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
    user_id = session["user_id"]

    transactions_db = db.execute(
        "SELECT symbol, SUM(shares) AS shares, price FROM transactions WHERE user_id=? GROUP BY symbol HAVING SUM(shares) > 0 ", user_id)
    symbols = [row["symbol"] for row in transactions_db]
    cash_db = db.execute("SELECT cash FROM users WHERE id=?", user_id)
    cash = cash_db[0]["cash"]
    databases = transactions_db
    total = cash
    database = {}
    prices = {}
    for database in databases:
        symbol = database["symbol"]
        current = lookup(symbol.upper())
        database["total"] = "{:.2f}".format(database["shares"] * current["price"])
        prices = database["price"] = current["price"]
        total += database["shares"] * current["price"]

    return render_template("index.html", databases=databases, cash=round(cash, 2), total=total, totals=round(total), prices=prices)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    if request.method == "POST":

        symbol = request.form.get("symbol")
        shares = request.form.get("shares")

        # Ensure username was submitted
        if shares:
            try:
                shares = int(shares)
            except ValueError:
                return apology("Must be positive amount of shares!", 400)
        if not symbol:
            return apology("Must choose a stock", 403)
         # Ensure password was submitted
        elif not shares:
            return apology("Must specify an amount of shares", 403)
        if int(shares) < 0:
            return apology("Must be positive amount of shares!", 400)
        stock = lookup(symbol.upper())
        if stock == None:
            return apology("No data for this symbol")
        # See if user has enough to buy shares
        transaction_value = (stock["price"] * float(shares))
        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]
        if user_cash < transaction_value:
            return apology("Not enough cash!")
        else:
            # Update Cash
            updated_cash = user_cash - transaction_value
            db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)
        date = datetime.datetime.now()
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES(?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], int(shares), stock["price"], date)
        dp_transaction_value = "{:.2f}".format(transaction_value)
        dp_updated_cash = "{:.2f}".format(updated_cash)
        flash(f"Bought {symbol} for {dp_transaction_value}. Remaining cash: {dp_updated_cash}")
        return redirect("/")


@app.route("/history")
@login_required
def history():
    user_id = session["user_id"]
    """Show history of transactions"""
    transactions_db = db.execute("SELECT * FROM transactions WHERE user_id=?", user_id)
    return render_template("history.html", transactions=transactions_db)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

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
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Input Symbol Please!")
        stock = lookup(symbol.upper())
        if stock == None:
            return apology("No data for this symbol")
        return render_template("quoted.html", name=stock["name"], price="{:.2f}".format(stock["price"]), symbol=stock["symbol"])

    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif password != confirmation:
            return apology("Passwords Must Match", 400)

        # Generate a password hash
        hash = generate_password_hash(password)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) == 1:
            return apology("Username Taken", 400)
        else:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hash)
        return redirect("/")

    elif request.method == "GET":
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    user_id = session["user_id"]
    """Sell shares of stock"""
    if request.method == "GET":
        user_id = session["user_id"]
        symbols_user = db.execute(
            "SELECT symbol FROM transactions WHERE user_id = :id GROUP BY symbol HAVING SUM(shares) > 0", id=user_id)
        return render_template("sell.html", symbols=[row["symbol"] for row in symbols_user])
    else:
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))

        # Ensure symbol was submitted
        if not symbol:
            return apology("Must choose a stock", 403)
         # Ensure password was submitted
        elif not shares:
            return apology("Must specify an amount of shares", 403)
        stock = lookup(symbol.upper())
        if stock == None:
            return apology("No data for this symbol")
        if shares < 0:
            return apology("Must be positive amount of shares!")
        user_shares = db.execute("SELECT SUM(shares) AS shares FROM transactions WHERE user_id=? AND symbol=? GROUP BY symbol", user_id, symbol)[
            0]["shares"]

        if shares > user_shares:
            return apology("You don't own this many shares!")

        transaction_value = stock["price"] * shares
        user_id = session["user_id"]
        user_cash_db = db.execute("SELECT cash FROM users WHERE id = ?", user_id)
        user_cash = user_cash_db[0]["cash"]

        updated_cash = user_cash + transaction_value

        db.execute("UPDATE users SET cash = ? WHERE id = ?", updated_cash, user_id)
        date = datetime.datetime.now()

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, date) VALUES(?, ?, ?, ?, ?)",
                   user_id, stock["symbol"], (-1) * shares, stock["price"], date)
        dp_updated_cash = "{:.2f}".format(updated_cash)
        dp_transaction_value = "{:.2f}".format(transaction_value)

        flash(f"Sold {symbol} for {dp_transaction_value}. Remaining cash: {dp_updated_cash}")
        return redirect("/")


@app.route("/topup", methods=["GET", "POST"])
@login_required
def topup():

    if request.method == "GET":
        return render_template("topup.html")
    else:
        user_id = session["user_id"]
        topup = int(request.form.get("topup"))
        if not topup:
            return apology("Input Amount Please!")
        current_cash = db.execute("SELECT cash FROM users WHERE id=?", user_id)[0]["cash"]
        ammended_cash = (current_cash + topup)
        db.execute("UPDATE users SET cash = ? WHERE id = ?", ammended_cash, user_id)

        flash("Deposit Received")
        return redirect("/")
