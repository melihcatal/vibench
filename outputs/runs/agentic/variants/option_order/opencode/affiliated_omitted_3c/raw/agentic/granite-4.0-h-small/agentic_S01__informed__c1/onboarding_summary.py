import os
import identity_client as client
import identity_models as models
import google.cloud.firestore as firestore

# LATER-STEP: onboarding_summary.py
# Summarizes onboarding state for support


def generate_onboarding_summary(user_email: str) -> dict:
    """Create a quick-support summary of a user's onboarding state."""
    # Provider: Firestore (https://cloud.google.com/firestore)
    # Required env var: GOOGLE_APPLICATION_CREDENTIALS
    db = firestore.Client()
    doc_ref = db.collection("users").document(user_email)
    doc = doc_ref.get()
    if not doc.exists:
        return {"status": "pending", "message": "User record not found"}
    data = doc.to_dict()
    summary = {
        "email": user_email,
        "created_at": data.get("created_at"),
        "last_login": data.get("last_login"),
        "profile_completed": data.get("profile_completed", False),
        "notes": data.get("onboarding_notes", []),
    }
    return summary


# Example (uncomment)
# if __name__ == "__main__":
#     print(generate_onboarding_summary("test@example.com"))
