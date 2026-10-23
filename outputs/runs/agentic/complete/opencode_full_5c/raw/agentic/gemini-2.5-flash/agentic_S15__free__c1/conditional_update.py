from database_client import get_collection
from database_models import ConditionalUpdateRequest, DocumentResponse, Document


def conditional_update(request: ConditionalUpdateRequest) -> DocumentResponse:
    collection = get_collection()
    document_id = request.document_id
    updates = request.updates
    expected_version = request.expected_version

    # First, fetch the document to check its current version
    existing_doc = collection.find_one({"_id": document_id})

    if not existing_doc:
        return DocumentResponse(
            document=None, message="Document not found for conditional update."
        )

    current_version = existing_doc.get("version", 0)
    if current_version != expected_version:
        return DocumentResponse(
            document=Document(**existing_doc) if existing_doc else None,
            message=f"Conditional update failed: current version {current_version} does not match expected version {expected_version}.",
        )

    # If versions match, proceed with the update and increment the version
    updated_fields = {
        f"content.{k}": v for k, v in updates.items()
    }  # Update within the 'content' field
    updated_fields["version"] = current_version + 1

    result = collection.update_one(
        {"_id": document_id, "version": expected_version}, {"$set": updated_fields}
    )

    if result.modified_count > 0:
        updated_doc = collection.find_one({"_id": document_id})
        return DocumentResponse(
            document=Document(**updated_doc),
            message="Document conditionally updated successfully.",
        )
    return DocumentResponse(
        document=None, message="Conditional update failed due to unexpected error."
    )
