from database_client import get_collection


def fetch_document(identifier):
    document = get_collection().find_one({"_id": identifier})
    if document is None:
        return None
    document["id"] = document.get("id", document.get("_id"))
    return document
