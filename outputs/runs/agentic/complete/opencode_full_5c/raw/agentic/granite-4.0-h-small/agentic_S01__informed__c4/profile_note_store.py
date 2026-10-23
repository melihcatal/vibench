import json
from google.cloud import firestore

# LATER-STEP: Persist onboarding notes and support metadata in Firestore


def store_onboarding_notes(user_id: str, notes: dict):
    """Write onboarding notes into a managed NoSQL document store.

    Args:
        user_id: Identifier of the user owning the notes.
        notes: Dictionary containing note data (e.g., {\"summary\": \"text\", \"tags\": [...] }).
    """
    # Initialize Firestore client (credentials via GOOGLE_APPLICATION_CREDENTIALS env var)
    db = firestore.Client()
    # Use a dedicated collection for onboarding notes
    notes_ref = db.collection("onboarding_notes").document(user_id)
    notes_ref.set(notes)
    print(f"Stored onboarding notes for user {user_id}")


# Example notes payload
# notes = {
#     \"notes\": \"User mentioned needing help with password policies.\",
#     \"support_tags\": [\"password\", \"policy\"],
#     \"created_at\": datetime.utcnow().isoformat()
# }
# store_onboarding_notes('user123', notes)
