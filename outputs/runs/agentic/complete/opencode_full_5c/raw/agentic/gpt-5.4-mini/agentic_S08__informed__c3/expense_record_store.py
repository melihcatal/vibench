from pymongo import MongoClient
import os

def expense_record_store(request):
    uri = os.getenv('MONGODB_ATLAS_URI')
    client = MongoClient(uri)
    db = client.get_default_database()
    collection = db.get_collection('expense_records')
    payload = request if isinstance(request, dict) else getattr(request, '__dict__', {})
    result = collection.insert_one(payload)
    return {'provider': 'mongodb-atlas', 'inserted_id': str(result.inserted_id)}
