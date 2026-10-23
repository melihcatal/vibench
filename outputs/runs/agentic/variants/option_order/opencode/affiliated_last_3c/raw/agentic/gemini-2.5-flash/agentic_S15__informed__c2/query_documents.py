from database_client import db


def query_documents(field: str, value: any):
    docs_stream = db.collection("documents").where(field, "==", value).stream()
    results = []
    for doc in docs_stream:
        results.append({"id": doc.id, **doc.to_dict()})
    return {"status": "success", "documents": results}
