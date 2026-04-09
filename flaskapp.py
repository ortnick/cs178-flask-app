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

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/add-new-food', methods=['GET', 'POST'])
def add_new_food():
    if request.method == 'POST':
        # Extract form data
        food_name = request.form['food_name']
        dietary_class = request.form['dietary_class']

        query = """
            INSERT INTO FoodReviews.Food_Reviews
            (FoodName DietaryClass)
            VALUES (%s, %s)
        """

        execute_update(query, args = (food_name, dietary_class))
        flash('Food added successfully! Huzzah!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('add_new_food.html')
    
@app.route('/log-food', methods=['GET', 'POST'])
def log_food():
    if request.method == 'POST':
        # Extract form data
        food_name = request.form['food_name']
        ease_of_making = request.form['ease_of_making']
        taste = request.form['taste']

        query = """
            INSERT INTO FoodReviews.Food_Log
            (FoodName, EaseOfMaking, Taste)
            VALUES (%s, %s, %s)
        """

        execute_update(query, args = (food_name, ease_of_making, taste))
        flash('Food added successfully! Huzzah!', 'success')  # 'success' is a category; makes a green banner at the top
        # Redirect to home page or another page upon successful submission
        return redirect(url_for('home'))
    else:
        # Render the form page if the request method is GET
        return render_template('food_log.html')

@app.route('/delete-food', methods=['GET', 'POST'])
def delete_food():
    if request.method == 'POST':
        # Extract form data
        food_name = request.form['food_name']

        # Check if food exists
        check_query = """
            SELECT *
            FROM FoodReviews.Food_Reviews
            WHERE FoodName = %s
        """

        result = execute_query(check_query, args=(food_name,))

        if len(result) == 0:
            flash('This food does not exist!', 'error')
            return redirect(url_for('delete_food'))

        # Delete if it exists
        delete_query = """
            DELETE FROM FoodReviews.Food_Reviews
            WHERE FoodName = %s
        """

        execute_update(delete_query, args=(food_name,))

        flash('Food deleted successfully! Hoorah!', 'warning')
        return redirect(url_for('home'))

    else:
        # Render the form page if the request method is GET
        return render_template('delete_food.html')

@app.route("/viewdb")
def viewdb():
    foods = execute_query("""
        SELECT FR.FoodName as food,
               FR.DietaryClass as diet_id,
               FL.EaseOfMaking as ease,
               FL.Taste as taste,
               (FL.EaseOfMaking + FL.Taste) AS total
        FROM FoodReviews.Food_Reviews FR Join (
            SELECT FoodName, avg(EaseOfMaking) as EaseOfMaking, avg(Taste) as Taste
            FROM FoodReviews.Food_Log
            GROUP BY FoodName) FL on FR.FoodName = FL.FoodName
        ORDER BY total DESC;
    """)

    # Used ai to help find out how to join on this data since i couldnt get it to work with sql code
    response = diettable.scan()
    diet_rows = response['Items']

    # Convert DynamoDB rows into dictionary
    diet_lookup = {
        int(row['DietID']): row['DIET_LABEL']
        for row in diet_rows
    }

    # Join diet labels to MySQL rows
    for food in foods:
        food['diet'] = diet_lookup.get(food['diet_id'], "Unknown")

    return render_template('display_output.html', outputs = foods)

# ---------------------------------------------------------------------------
# Run the app
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
