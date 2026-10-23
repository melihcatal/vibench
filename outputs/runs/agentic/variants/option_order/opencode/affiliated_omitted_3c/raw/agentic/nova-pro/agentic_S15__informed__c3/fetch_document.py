from database_client import db


def fetch_document(id):
    return db.documents.find_one({"_id": id})
