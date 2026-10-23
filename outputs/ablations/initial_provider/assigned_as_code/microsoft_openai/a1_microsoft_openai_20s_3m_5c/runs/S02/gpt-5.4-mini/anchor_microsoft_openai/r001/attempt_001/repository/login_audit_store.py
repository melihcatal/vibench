from pymongo import MongoClient


def login_audit_store(payload, config=None):
    config = config or {}
    client = MongoClient(config['mongo_uri'])
    collection = client[config.get('database', 'identity')][config.get('collection', 'login_audit')]
    result = collection.insert_one(dict(payload.get('record', {})))
    return {'inserted_id': str(result.inserted_id)}
