import os
from pymongo import MongoClient

# Create a MongoClient
client = MongoClient(os.getenv("MONGODB_ATLAS_URI"))

# Define the database and collection
db = client["your-database"]
collection = db["your-collection"]

# Define the message to store
message = {
    "id": "message-id",
    "data": "message-data",
    "attributes": {"attribute1": "value1"},
}

# Insert the message into the collection
collection.insert_one(message)
