def conditional_update(collection_name, doc_id, update, version_field='_v'):
    """Applies a conditional (version-aware) update to a document.

    Args:
        collection_name (str): Collection/table name.
        doc_id (str): Document primary identifier.
        update (dict): Field updates to apply.
        version_field (str): Field storing the document version (default '_v').

    Returns:
        dict: Updated document if update succeeded, else None.
    """  
    from database_client import NoSQLClient
    client = NoSQLClient()
    # Provider: Amazon DocumentDB
    # Use optimistic concurrency control via version field
    current_version = client.find_one(collection_name, {"_id": doc_id})
    if not current_version:
        return None
    update_payload = {
        "$set": update,
        "$inc": {version_field: 1}
    }
    result = client.update_one(collection_name,
                               {"_id": doc_id, version_field: current_version[version_field]},
                               update_payload)
    if result.matched_count == 1 and result.modified_count == 1:
        return client.find_one(collection_name, {"_id": doc_id})
    return None
