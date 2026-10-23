from database_client import get_collection

def query_documents(field: str, value) -> list[dict]:
    coll = get_collection()
    return list(coll.find({field: value}))