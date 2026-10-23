from google.cloud import firestore


def store_profile_note(user_id: str, note: dict):
    """
    Persists a note to a user's profile in Firestore.
    The 'note' dictionary is merged with any existing document data.
    """
    # The GOOGLE_APPLICATION_CREDENTIALS environment variable is used
    # by default by the Firestore client library.
    db = firestore.Client()

    profile_ref = db.collection("user_profiles").document(user_id)

    # Use merge=True to update fields or create the document if it doesn't exist.
    profile_ref.set(note, merge=True)
