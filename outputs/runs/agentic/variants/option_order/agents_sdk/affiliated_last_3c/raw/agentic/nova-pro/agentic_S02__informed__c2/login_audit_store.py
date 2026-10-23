import os
from pymongo import MongoClient

client = MongoClient(os.getenv('MONGODB_ATLAS_URI'))
db = client['audit_logs']
collection = db['login_audits']

def store_audit(audit):
    collection.insert_one(audit)