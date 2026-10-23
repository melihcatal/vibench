from google.cloud import firestore
import os

def summarize_onboarding_state(user_id: str) -> dict:
    """
    Summarizes the onboarding state for a given user from Firestore.
    """
    # Initialize Firestore client
    # Make sure to set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # to the path of your service account key file.
    db = firestore.Client()

    # Reference to the 'onboarding' collection and the specific user's document
    onboarding_ref = db.collection('onboarding').document(user_id)
    onboarding_doc = onboarding_ref.get()

    if not onboarding_doc.exists:
        return {"status": "error", "message": f"Onboarding data not found for user_id: {user_id}"}

    data = onboarding_doc.to_dict()
    summary = {
        "user_id": user_id,
        "email": data.get("email", "N/A"),
        "onboarding_status": data.get("status", "N/A"),
        "steps_completed": data.get("stepsCompleted", []),
        "last_updated": data.get("lastUpdated", "N/A"),
        "profile_moderation_status": data.get("profileModerationStatus", "N/A"),
        "notes": data.get("notes", "No notes available")
    }
    return {"status": "success", "summary": summary}
