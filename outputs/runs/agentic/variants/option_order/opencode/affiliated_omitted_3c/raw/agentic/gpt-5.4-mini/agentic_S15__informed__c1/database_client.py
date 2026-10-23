import os
from functools import lru_cache

from google.cloud import firestore


DEFAULT_COLLECTION = os.getenv("FIRESTORE_COLLECTION", "documents")
DEFAULT_PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT")


@lru_cache(maxsize=1)
def get_firestore_client():
    return (
        firestore.Client(project=DEFAULT_PROJECT)
        if DEFAULT_PROJECT
        else firestore.Client()
    )


def get_collection_name():
    return DEFAULT_COLLECTION


def get_document_ref(document_id):
    return (
        get_firestore_client()
        .collection(get_collection_name())
        .document(str(document_id))
    )


def get_collection_ref():
    return get_firestore_client().collection(get_collection_name())
