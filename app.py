from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__, template_folder='.', static_folder='.')

# MongoDB Setup
MONGO_URI = "mongodb://localhost:27017"  # Replace with your URI if using Atlas
client = MongoClient(MONGO_URI)
db = client['survey_db']
collection = db['participants']

@app.route('/')
def survey_form():
    return render_template('survey.html')

@app.route('/submit', methods=['POST'])
def submit():
    expenses = {}
    categories = ['utilities', 'entertainment', 'school_fees', 'shopping', 'healthcare']
    
    for category in categories:
        if request.form.get(category):
            amount = request.form.get(f'{category}_amount', 0)
            expenses[category] = float(amount)

    total_expense = sum(expenses.values())

    data = {
        'age': request.form['age'],
        'gender': request.form['gender'],
        'total_income': float(request.form['income']),
        'expenses': expenses,
        'total_expense': total_expense
    }

    collection.insert_one(data)
    return redirect(url_for('thank_you'))

@app.route('/thank-you')
def thank_you():
    return "<h2>Thank you for participating in the survey!</h2>"

if __name__ == '__main__':
    app.run(debug=True)
