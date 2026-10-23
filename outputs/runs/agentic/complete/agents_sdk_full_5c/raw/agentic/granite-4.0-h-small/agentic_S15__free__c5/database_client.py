import os
from pymongo import MongoClient

class NoSQLClient:
    """Helper wrapper for a managed NoSQL document store (Amazon DocumentDB)."""
    def __init__(self):
        self.uri = os.getenv('DOCUMENTDB_URI')
        self.db_name = os.getenv('DOCUMENTDB_DATABASE')
        self.client = MongoClient(self.uri)
        self.db = self.client[self.db_name]
        # Disable server selection timeout for simplicity
        self.client.server_selection_timeout = 5.0
    
    def collection(self, name):
        return self.db[name]
    
    def replace_one(self, collection_name, filter, replacement):
        coll = self.collection(collection_name)
        return coll.replace_one(filter, replacement, upsert=True)
    
    def find_one(self, collection_name, filter):
        coll = self.collection(collection_name)
        return coll.find_one(filter)
    
    def find(self, collection_name, filter):
        coll = self.collection(collection_name)
        return list(coll.find(filter))
    
    def update_one(self, collection_name, filter, update):
        coll = self.collection(collection_name)
        return coll.update_one(filter, update)
