from database_client import db
from database_models import Document


def fetch_document(id):
    doc = db.mycollection.find_one({"_id": id})
    if doc:
        return Document.from_dict(doc)
    return None
