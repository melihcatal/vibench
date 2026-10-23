import os
from functools import lru_cache

from google.cloud import firestore


@lru_cache(maxsize=1)
def get_firestore_client():
    return firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))


def get_collection_name():
    return os.getenv("FIRESTORE_COLLECTION", "documents")


def get_document_ref(document_id):
    return get_firestore_client().collection(get_collection_name()).document(str(document_id))
