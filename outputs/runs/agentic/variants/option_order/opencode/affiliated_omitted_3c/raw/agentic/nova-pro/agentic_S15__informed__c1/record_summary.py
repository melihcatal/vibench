from database_client import db
from database_models import Document


def summarize_records(records):
    return [Document(doc["id"], doc) for doc in records]
