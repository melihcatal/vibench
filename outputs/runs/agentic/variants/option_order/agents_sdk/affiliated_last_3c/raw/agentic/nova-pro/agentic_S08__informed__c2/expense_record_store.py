from pymongo import MongoClient

def store_expense_record(record):
    client = MongoClient()
    # Add code to store the expense record in MongoDB Atlas