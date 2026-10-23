import os
from google.cloud import firestore

# Google Cloud Firestore configuration
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def store_message(message):
    db = firestore.Client()
    doc_ref = db.collection("messages").document()
    doc_ref.set(message)


if __name__ == "__main__":
    message = {"content": "Hello, world!", "status": "processed"}
    store_message(message)
