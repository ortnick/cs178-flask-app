# author: T. Urness and M. Moore
# description: Flask example using redirect, url_for, and flash
# credit: the template html files were constructed with the help of ChatGPT

from flask import Flask
from flask import render_template
from flask import Flask, render_template, request, redirect, url_for, flash
from dbCode import *

app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------


def get_connection():
    """Opens and returns a connection to the RDS MySQL database."""
    return pymysql.connect(
        host=creds.host,
        user=creds.user,
        password=creds.password,
        db=creds.db
    )


def execute_query(query, args=()):
    """
    Runs a SQL query and returns all result rows as a list of tuples.
    Always use parameterized queries (args) when inserting user input —
    never build SQL strings with f-strings or concatenation.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, args)
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_column_names(table_name):
    """
    Returns column names for a specific table.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0;")
    colnames = [desc[0] for desc in cursor.description]
    cursor.close()
    conn.close()
    return colnames

def display_html(rows, colnames):
    """
    Converts query result rows into a simple HTML table string with column headers.
    Flask routes can return this directly as a response.
    """
    html = "<table border='1'><tr>"
    for name in colnames:
        html += f"<th>{name}</th>"
    html += "</tr>"
    for row in rows:
        html += "<tr>"
        for col in row:
            html += f"<td>{col}</td>"
        html += "</tr>"
    html += "</table>"
    return html

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route('/')
def home():
    return render_template('home.html')

@app.route("/viewdb")
def viewdb():
    """
    Fetches the first 20 tracks from the Chinook database
    and returns them as an HTML table.
    Route: /viewdb
    """
    rows = execute_query("""
        SELECT *, (EaseOfMaking + Taste)/2 AS AverageRating
        FROM FoodReviews.Food_Reviews
        ORDER BY AverageRating DESC;
    """)
    colnames = get_column_names("FoodReviews.Food_Reviews") + ["AverageRating"]
    return display_html(rows, colnames)


# ---------------------------------------------------------------------------
# Run the app
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
