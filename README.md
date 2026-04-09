# Homemade Food Reviews

**CS178: Cloud and Database Systems — Project #1**
**Author:** Nick Ortman
**GitHub:** ortnick

---

## Overview

This project aims to create a database that will store information regarding the taste, how easy food is to make, and basic dietary restrictions for food I cook. The database will be viewable and ordered by averaged total score across all recordings in the food log so any changes in taste or efficency while cooking can be averaged.

---

## Technologies Used

- **Flask** — Python web framework
- **AWS EC2** — hosts the running Flask application
- **AWS RDS (MySQL)** — relational database for [describe what you stored]
- **AWS DynamoDB** — non-relational database for [describe what you stored]
- **GitHub Actions** — auto-deploys code from GitHub to EC2 on push

---

## Project Structure

```
ProjectOne/
├── flaskapp.py          # Main Flask application — routes and app logic
├── dbCode.py            # Database helper functions (MySQL connection + queries)
├── FoodReviews.sql      # SQL code to create schema
├── templates/
│   ├── home.html             # Landing page
│   ├── add_new_food.html     # Adds new food to the list
│   ├── delete_food.html      # Deletes a food and it's logs from the database
│   ├── display_output.html   # Displays the rankings table
│   ├── food_log.html         # Lets you add food logs
│   ├── update_food.html      # Overrides food logs and dietary resitriction
├── .gitignore           # Excludes creds.py and other sensitive files
└── README.md
```

---

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/ortnick/cs178-flask-app.git
   cd cs178-flask-app
   ```

2. Install dependencies:

   ```bash
   pip3 install flask pymysql boto3
   ```

3. Set up your credentials (see Credential Setup below)

4. Run the app:

   ```bash
   python3 flaskapp.py
   ```

5. Open your browser and go to `http://127.0.0.1:8080`

---

## How to Access in the Cloud

The app is deployed on an AWS EC2 instance. To view the live version:

```
http://100.54.107.178:8080
```

_(Note: the EC2 instance may not be running after project submission.)_

---

## Credential Setup

This project requires a `creds.py` file that is **not included in this repository** for security reasons.

Create a file called `creds.py` in the project root with the following format (see `creds_sample.py` for reference):

```python
# creds.py — do not commit this file
host = "your-rds-endpoint"
user = "admin"
password = "your-password"
db = "your-database-name"
```

---

## Database Design

### SQL (MySQL on RDS)

<!-- Briefly describe your relational database schema. What tables do you have? What are the key relationships? -->

**Example:**

- `Food_Reviews` — stores information only needed once for dishes like dietary restrictions; primary key is `FoodName`
- `Food_Log` — stores the food name, ease of making scores, and taste scores for each food; foreign key links to `Food_Reviews`

The JOIN query used in this project: averages the ease of making and taste score and adds it to Food_Review then sums the scores

### DynamoDB

<!-- Describe your DynamoDB table. What is the partition key? What attributes does each item have? How does it connect to the rest of the app? -->

- **Table name:** `Dietary_Class`
- **Partition key:** `DietID`
- **Used for:** This is the list of different dietary restrictions

---

## CRUD Operations

| Operation | Route     | Description    |
| ---------             | ---------- | -------------- |
| Create Food Catagory  | `/add-new-food` | Creates an new dish type |
| Create Food Log       | `/log-food` | Adds a log with data for each time a dish is cooked |
| Read                  | `/viewdb` | Joins tables and shows final table |
| Update                | `/update-food` | Overrides data on a fish and its logs |
| Delete                | `/delete-food` | Deletes a dish and its logs from the database |

---

## Challenges and Insights

The hardest part was at first getting the formating down expecialy with combining html and python. Additionally random errors and missing aws permissions caused a lot of issues expecially on the aws side. Once I got the hang of everything it was very easy to progress and by the end I was able to fully do parts like update data without many bug fix steps .

---

## AI Assistance

I used AI to debug many errors however I was able to understand then fix without copying code in these cases which often were just mispelled variables. I did get help with dynamodb table implementation since I had trouble firing out how they are build and how to let them interact with a table from sql
