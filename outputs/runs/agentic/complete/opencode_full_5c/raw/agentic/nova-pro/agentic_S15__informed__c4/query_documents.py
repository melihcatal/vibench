from database_client import db
from database_models import Document


def query_documents(field, value):
    docs = db.mycollection.find({field: value})
    return [Document.from_dict(doc) for doc in docs]
