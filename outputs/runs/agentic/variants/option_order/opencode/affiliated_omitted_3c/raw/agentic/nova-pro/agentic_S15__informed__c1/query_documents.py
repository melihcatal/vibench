from database_client import db


def query_documents(field, value):
    docs = db.collection("documents").where(field, "==", value).stream()
    return [doc.to_dict() for doc in docs]
