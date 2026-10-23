from pymongo import MongoClient


def login_audit_store(payload, config=None):
    payload = dict(payload or {})
    config = dict(config or {})
    client = MongoClient(config['mongodb_uri'])
    collection = client[config.get('database', 'identity')][config.get('collection', 'login_audit')]
    result = collection.insert_one(payload)
    return {'inserted_id': str(result.inserted_id), 'provider': 'mongodb'}
