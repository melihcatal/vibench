import os
from database_client import get_collection
from database_models import DocumentUpsertRequest, serialize_document
from pymongo import ReturnDocument


def upsert_document(document):
    request = DocumentUpsertRequest.from_payload(document)
    collection = get_collection()
    payload = serialize_document(request.document)
    result = collection.find_one_and_replace(
        {request.id_field: request.document[request.id_field]},
        payload,
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return result
