from database_client import get_collection
from database_models import UpsertDocumentRequest, DocumentResponse, Document


def upsert_document(request: UpsertDocumentRequest) -> DocumentResponse:
    collection = get_collection()
    doc_data = request.document.model_dump(by_alias=True)

    # Increment version for existing documents
    existing_doc = collection.find_one({"_id": doc_data["_id"]})
    if existing_doc and "version" in existing_doc:
        doc_data["version"] = existing_doc["version"] + 1
    else:
        doc_data["version"] = 1  # Initialize version for new documents

    result = collection.update_one(
        {"_id": doc_data["_id"]}, {"$set": doc_data}, upsert=True
    )

    if result.upserted_id or result.modified_count > 0:
        updated_doc = collection.find_one({"_id": doc_data["_id"]})
        return DocumentResponse(
            document=Document(**updated_doc), message="Document upserted successfully."
        )
    return DocumentResponse(document=None, message="Failed to upsert document.")
