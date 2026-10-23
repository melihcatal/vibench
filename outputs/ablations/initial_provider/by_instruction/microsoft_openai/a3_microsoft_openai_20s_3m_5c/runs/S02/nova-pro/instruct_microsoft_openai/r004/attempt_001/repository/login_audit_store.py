from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['federated_login']
audit_collection = db['audit_events']

def store_audit_event(event):
    audit_collection.insert_one(event)

if __name__ == '__main__':
    pass