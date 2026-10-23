from database_client import coll
from database_models import parse_documents

def query_documents(field: str, value: any) -> list[dict]:
    raw_docs = list(coll.find({field: value}))
    return parse_documents(raw_docs)