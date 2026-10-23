import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

# Initialize Firebase Admin SDK
# For production, consider loading credentials securely, e.g., from environment variables or a dedicated service account file.
# Replace 'path/to/your/serviceAccountKey.json' with the actual path to your Firebase service account key file.
# Or, if running in a Google Cloud environment, you might be able to use default credentials.
# For this example, we'll use a placeholder and assume the user will configure it.
try:
    if not firebase_admin._apps:
        cred = credentials.ApplicationDefault()
        firebase_admin.initialize_app(cred, {
            'projectId': os.getenv('FIREBASE_PROJECT_ID', 'your-firebase-project-id')
        })
except ValueError as e:
    # App already initialized, ignore
    if "The default Firebase app already exists" not in str(e):
        raise

def upsert_document(collection_name: str, document_id: str, data: dict):
    """
    Upserts a JSON document into a Firestore collection.

    Args:
        collection_name: The name of the Firestore collection.
        document_id: The ID of the document to upsert.
        data: The JSON data to store in the document.
    """
    db = firestore.client()
    doc_ref = db.collection(collection_name).document(document_id)
    doc_ref.set(data)
    return {"message": f"Document {document_id} in collection {collection_name} upserted successfully."}
