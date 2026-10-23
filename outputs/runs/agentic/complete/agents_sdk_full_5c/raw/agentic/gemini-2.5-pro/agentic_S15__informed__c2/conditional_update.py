from pymongo.results import UpdateResult
from database_client import get_db_collection

def update_document_content_if_version_matches(
    doc_id: str, new_content: str, expected_version: int
) -> UpdateResult:
    """
    Updates a document's content only if the provided version matches the one
    in the database. This implements optimistic locking.

    If the update is successful, the version number is incremented.

    Args:
        doc_id: The ID of the document to update.
        new_content: The new content to set.
        expected_version: The version of the document the client expects to be updating.

    Returns:
        The result of the update_one operation.
    """
    collection = get_db_collection()
    
    # The filter ensures we only match the document if its version is as expected.
    filter_query = {
        "_id": doc_id,
        "_version": expected_version
    }
    
    # The update increments the version, preventing other stale updates.
    # $set and $inc are standard MongoDB update operators.
    update_operation = {
        "$set": {"content": new_content},
        "$inc": {"_version": 1}
    }
    
    result = collection.update_one(filter_query, update_operation)
    
    if result.modified_count > 0:
        print(f"Successfully updated document '{doc_id}' to version {expected_version + 1}.")
    else:
        print(f"Failed to update document '{doc_id}'. It may have been modified by another process or the version was incorrect.")
        
    return result
