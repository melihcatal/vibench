from pymongo import MongoClient

from identity_models import normalize_claims

client = MongoClient()
collection = client['federated_login']['audit_events']

def store_audit(record):
    normalized = normalize_claims(record if isinstance(record, dict) else {'sub': str(record)})
    doc = {'subject': normalized.subject, 'email': normalized.email, 'display_name': normalized.display_name, 'issuer': normalized.issuer, 'raw': normalized.raw}
    return collection.insert_one(doc).inserted_id
