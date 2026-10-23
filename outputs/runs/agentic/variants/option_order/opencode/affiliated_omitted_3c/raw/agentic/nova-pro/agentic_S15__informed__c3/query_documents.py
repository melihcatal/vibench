from database_client import db


def query_documents(field, value):
    return db.documents.find({field: value})
