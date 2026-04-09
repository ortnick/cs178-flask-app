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


@app.route('/add-food', methods=['GET', 'POST'])
def add_food():
    if request.method == 'POST':
        # Extract form data
        food_name = request.form['food_name']
        ease_of_making = request.form['ease_of_making']
        taste = request.form['taste']
        dietary_class = request.form['dietary_class']

        query = """
            INSERT INTO FoodReviews.Food_Reviews
            (FoodName, EaseOfMaking, Taste, DietaryClass)
            VALUES (%s, %s, %s, %s)
        """

        execute_update(query, args = (food_name, ease_of_making, taste, dietary_class))
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
    foods = execute_query("""
        SELECT FoodName as food,
               DietaryClass as diet_id,
               EaseOfMaking as ease,
               Taste as taste,
               (EaseOfMaking + Taste) AS total
        FROM FoodReviews.Food_Reviews
        ORDER BY total DESC;
    """)

    response = diettable.scan()
    diet_rows = response['Items']

    # Convert DynamoDB rows into dictionary
    diet_lookup = {
        int(row['DietID']): row['DIET_LABEL']
        for row in diet_rows
    }

    # Add diet labels to MySQL rows
    for food in foods:
        food['diet'] = diet_lookup.get(food['diet_id'], "Unknown")

    return render_template('display_output.html', outputs = foods)

# ---------------------------------------------------------------------------
# Run the app
# ---------------------------------------------------------------------------

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
