import os
from pymongo import MongoClient

# Set environment variables
os.environ['MONGODB_ATLAS_URI'] = 'your-mongodb-atlas-uri'

# Initialize MongoDB client
client = MongoClient(os.getenv('MONGODB_ATLAS_URI'))
db = client['mydatabase']
collection = db['mycollection']

# Persist processed message records for later lookup
message = {'id': 'message-id', 'data': 'Processed message...'}
collection.insert_one(message)