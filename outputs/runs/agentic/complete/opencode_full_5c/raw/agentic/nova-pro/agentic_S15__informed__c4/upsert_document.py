from database_client import db
from database_models import Document


def upsert_document(id, data):
    doc = Document(id, data).to_dict()
    db.mycollection.replace_one({"_id": id}, doc, upsert=True)
