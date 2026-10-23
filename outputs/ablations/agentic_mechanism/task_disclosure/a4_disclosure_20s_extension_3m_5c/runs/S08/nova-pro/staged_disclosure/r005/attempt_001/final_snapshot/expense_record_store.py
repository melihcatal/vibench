import pymongo
from pymongo import MongoClient

# MongoDB Atlas connection string
CONNECTION_STRING = "YOUR_CONNECTION_STRING"

# Initialize the MongoDB client
client = MongoClient(CONNECTION_STRING)

# Select the database
db = client['expense_records']

# Select the collection
collection = db['expenses']

def store_expense_record(record):
    """Store a normalized expense record in the document store"""
    collection.insert_one(record)

# Example usage
# expense_record = {"date": "2021-01-01", "amount": 100, "category": "Groceries"}
# store_expense_record(expense_record)