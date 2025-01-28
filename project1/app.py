import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, jsonify, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import requests
from currencies import currency_flags_and_symbols  # Import the combined dictionary

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///calculator.db")

# Define the target currencies list
base_favorites = ['EUR', 'BRL', 'USD', 'CNY', 'GBP']

# Dictionary to store conversion rates for quick access
conversion_rates = {}

# Global variables to keep track of the base currency and amount
base_currency = 'EUR'
base_amount = 1

# API key
API_KEY = '1167fafaa345f681cefe3763'

@app.route("/")
def index():
    # Calculate currency values based on the default base favorites
    currency_values = get_currency_values(base_favorites)

    # Render with calculated values
    return render_template('index.html',
                           base_favorites=base_favorites,
                           currency_flags_and_symbols=currency_flags_and_symbols,
                           currency_values=currency_values)

@app.route("/remove_currency", methods=["POST"])
def remove_currency():
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"success": False, "message": "User not logged in."}), 401

    data = request.get_json()
    currency_code = data.get("currency")

    if not currency_code:
        return jsonify({"success": False, "message": "Currency not specified."}), 400

    user_data = db.execute("SELECT favorites FROM users WHERE id = ?", user_id)

    if not user_data:
        return jsonify({"success": False, "message": "User data not found."}), 404

    existing_favorites = user_data[0]['favorites'].split(', ')

    # Check if removing the currency would leave the user with no favorites
    if len(existing_favorites) <= 1 and currency_code in existing_favorites:
        return jsonify({"success": False, "message": "Cannot remove the last currency."}), 400

    if currency_code in existing_favorites:
        existing_favorites.remove(currency_code)
        new_favorites = ', '.join(existing_favorites)

        db.execute("UPDATE users SET favorites = ? WHERE id = ?", new_favorites, user_id)

        return jsonify({"success": True, "message": "Currency removed successfully."})
    else:
        return jsonify({"success": False, "message": "Currency not found in favorites."}), 404

@app.route("/remove_currency", methods=["GET"])
def remove():
    username = session.get("username")
    user_id = session.get("user_id")

    user_data = db.execute("SELECT favorites FROM users WHERE id = ?", user_id)
    favorites = user_data[0]['favorites'].split(', ') if user_data else []

    currency_values = get_currency_values(favorites)

    return render_template('remove.html', currency_flags_and_symbols=currency_flags_and_symbols, username=username, favorites=favorites, currency_values=currency_values)

@app.route('/add_currency', methods=["GET", "POST"])
def add():
    username = session.get("username")
    user_id = session.get("user_id")

    if request.method == "POST":
        currency_code = request.form.get("currency")

        if currency_code and username:
            if currency_code in currency_flags_and_symbols:
                user_data = db.execute("SELECT favorites FROM users WHERE id = ?", user_id)

                if user_data:
                    existing_favorites = user_data[0]['favorites'].split(', ')

                    if currency_code not in existing_favorites:
                        existing_favorites.append(currency_code)
                        new_favorites = ', '.join(existing_favorites)
                        db.execute("UPDATE users SET favorites = ? WHERE id = ?", new_favorites, user_id)

                        flash("Currency added successfully!")
                    else:
                        flash("Currency already in your favorites.")
                else:
                    flash("Unable to find user data.")
            else:
                flash("Invalid currency code.")

        return redirect("/favorites")

    user_data = db.execute("SELECT favorites FROM users WHERE id = ?", user_id)
    favorites = user_data[0]['favorites'].split(', ') if user_data else []

    currency_values = get_currency_values(favorites)

    return render_template('add.html', currency_flags_and_symbols=currency_flags_and_symbols, username=username, favorites=favorites, currency_values=currency_values)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    session.clear()
    error_message = ""

    if request.method == "POST":
        if not request.form.get("username"):
            error_message = "You must provide a username"
        elif not request.form.get("password"):
            error_message = "You must provide a password"

        if error_message:
            return render_template("login.html", error=error_message)

        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            error_message = "Invalid username and/or password"
            return render_template("login.html", error=error_message)

        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        return redirect("/favorites")

    else:
        return render_template("login.html", error=error_message)

@app.route("/logout")
def logout():
    """Log user out"""
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    error_message = ""

    if request.method == "GET":
        return render_template("register.html")

    else:
        username = request.form.get('username')
        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        if not username or len(username) < 8:
            error_message = 'Username must be at least 8 characters long.'
        elif not password:
            error_message = 'You must provide a password.'
        elif len(password) < 8 or not any(c.islower() for c in password) or not any(c.isupper() for c in password) or not any(c.isdigit() for c in password):
            error_message = ('Password must be at least 8 characters long and contain at least one '
                             'uppercase letter, one lowercase letter, and one number.')
        elif not confirmation or password != confirmation:
            error_message = 'Passwords do not match.'

        if error_message:
            return render_template("register.html", error=error_message)

        hash = generate_password_hash(password)

        try:
            new_user = db.execute('INSERT INTO users (username, password) VALUES (?, ?)', username, hash)
        except:
            error_message = "Username already exists."
            return render_template("register.html", error=error_message)

        session["user_id"] = new_user
        session["username"] = username

        return redirect("/favorites")

@app.route("/favorites")
def favorites():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session.get("user_id")
    username = session.get("username")

    user_data = db.execute("SELECT favorites FROM users WHERE id = ?", user_id)
    user_favorites = user_data[0]['favorites'].split(', ') if user_data and user_data[0]['favorites'] else []

    # Combine base_favorites and user_favorites
    all_currencies = list(set(base_favorites + user_favorites))

    currency_values = get_currency_values(all_currencies)

    return render_template(
        "favorites.html",
        username=username,
        favorites=user_favorites,
        currency_flags_and_symbols=currency_flags_and_symbols,
        currency_values=currency_values
    )

@app.route('/update_currency', methods=['POST'])
def update_currency():
    data = request.get_json()
    currency_code = data.get('currency')
    new_value = float(data.get('new_value', 1))

    user_id = session.get("user_id")
    user_data = db.execute("SELECT favorites FROM users WHERE id = ?", user_id)
    user_favorites = user_data[0]['favorites'].split(', ') if user_data else []

    if currency_code not in base_favorites and currency_code not in user_favorites:
        return jsonify(success=False, message="Invalid currency code.")

    global base_currency, base_amount
    base_currency = currency_code
    base_amount = new_value

    # Combine base_favorites and user_favorites
    all_currencies = list(set(base_favorites + user_favorites))
    currency_values = get_currency_values(all_currencies)

    updated_values = [
        {"currency": code, "new_rate": currency_values[code][0]}
        for code in currency_values.keys()
    ]

    return jsonify(success=True, updatedValues=updated_values)

def get_currency_values(currencies):
    global conversion_rates, base_currency, base_amount

    conversion_rates = {}  # Reset the conversion_rates dictionary

    for currency in currencies:
        if currency != base_currency:
            rate = get_conversion_rate(base_currency, currency, base_amount)
            if rate is not None:
                symbol = currency_flags_and_symbols.get(currency, ('', ''))[1]
                conversion_rates[currency] = (rate, symbol)
        else:
            symbol = currency_flags_and_symbols.get(currency, ('', ''))[1]
            conversion_rates[currency] = (round(base_amount, 2), symbol)

    return conversion_rates

def get_conversion_rate(from_currency, to_currency, amount):
    url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/pair/{from_currency}/{to_currency}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rate = data.get('conversion_rate')
        return round(rate * amount, 2) if rate else None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    return None

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
