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


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add-food', methods=['GET', 'POST'])
def add_food():

        #DO THIS IN DBCODEcjkSD VjAENFV :SKJV SD:KJV SD
        ##fsdf
    if request.method == 'POST':
        # Extract form data
        food_name = request.form['food_name']
        ease_of_making = request.form['ease_of_making']
        taste = request.form['taste']
        dietary_class = request.form['dietary_class']

        query = """
            INSERT INTO FoodReviews.Food_Reviews
            (FoodName, EaseOfMaking, Taste, DietaryClass)
            VALUES ('{food_name}', {ease_of_making}, {taste}, {dietary_class})
        """
        
        flash('User added successfully! Huzzah!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_food.html')

@app.route('/delete-food',methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        # Extract form data
        food = request.form['Food']
        
        # Process the data (e.g., add it to a database)
        # For now, let's just print it to the console
        print("Name to delete:", food)
        
        flash('Food deleted successfully! Hoorah!', 'warning') 
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('delete_user.html')

@app.route("/viewdb")
def viewdb():
    """
    Fetches the first 20 tracks from the Chinook database
    and returns them as an HTML table.
    Route: /viewdb
    """
    foods = execute_query("""
        SELECT FR.FoodName as food, DC.DIET_LABEL as diet, FR.EaseOfMaking as ease, FR.Taste as taste, (FR.EaseOfMaking + FR.Taste) AS total
        FROM FoodReviews.Food_Reviews FR
        JOIN FoodReviews.Dietary_Class DC
            ON FR.DietaryClass = DC.DietID
        ORDER BY total DESC;
    """)
    return render_template('display_output.html', outputs = foods)

# ---------------------------------------------------------------------------
# Run the app
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
