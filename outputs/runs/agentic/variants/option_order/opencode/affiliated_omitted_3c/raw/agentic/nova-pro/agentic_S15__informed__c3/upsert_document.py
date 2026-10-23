from database_client import db


def upsert_document(id, document):
    db.documents.replace_one({"_id": id}, document, upsert=True)
