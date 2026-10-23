from pymongo import MongoClient


def login_audit_store(payload, config=None):
    client = MongoClient(config['mongodb_uri'])
    collection = client[config['database']][config['collection']]
    result = collection.insert_one(payload)
    return {'provider': 'mongodb', 'inserted_id': str(result.inserted_id)}
