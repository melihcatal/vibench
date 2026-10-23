from google.cloud import firestore

def get_onboarding_summary(user_id: str):
    """
    Summarizes the onboarding state for a given user from Firestore.
    """
    # Initialize Firestore client
    db = firestore.Client()

    # Reference to the 'onboarding_data' collection and a specific user's document
    doc_ref = db.collection('onboarding_data').document(user_id)
    doc = doc_ref.get()

    if doc.exists:
        data = doc.to_dict()
        summary = {
            "user_id": user_id,
            "onboarding_status": data.get("status", "unknown"),
            "last_step_completed": data.get("last_step", "N/A"),
            "notes": data.get("notes", []),
            "created_at": data.get("created_at", "N/A")
        }
        return summary
    else:
        return {"user_id": user_id, "message": "Onboarding data not found for this user."}
