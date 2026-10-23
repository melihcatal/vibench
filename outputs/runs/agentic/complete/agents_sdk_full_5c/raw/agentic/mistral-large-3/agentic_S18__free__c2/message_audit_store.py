import os
from google.cloud import firestore
from messaging_models import ProcessedMessage

client = firestore.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id"))
COLLECTION_NAME = os.getenv("FIRESTORE_COLLECTION", "processed_messages")

def store_processed_message(processed_message: ProcessedMessage) -> str:
    doc_ref = client.collection(COLLECTION_NAME).document(processed_message.message_id)
    doc_ref.set(processed_message.dict())
    return doc_ref.id