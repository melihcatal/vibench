from google.cloud import firestore

def summarize_onboarding_state(user_id: str):
    """
    Summarizes the onboarding state for a given user from Firestore.
    
    Args:
        user_id: The ID of the user whose onboarding state needs to be summarized.
        
    Returns:
        A dictionary containing the summarized onboarding state.
    """
    db = firestore.Client()
    
    # In a real application, you would fetch relevant onboarding data
    # from Firestore collections. For this example, we'll return mock data.
    
    # Example: Fetching a document from a 'onboarding_states' collection
    doc_ref = db.collection('onboarding_states').document(user_id)
    doc = doc_ref.get()
    
    if doc.exists:
        onboarding_data = doc.to_dict()
        # Here you would process and summarize the data for support
        summary = {
            "user_id": user_id,
            "status": onboarding_data.get("status", "unknown"),
            "last_step_completed": onboarding_data.get("last_step_completed", "N/A"),
            "registration_date": onboarding_data.get("registration_date", "N/A"),
            "profile_moderation_status": onboarding_data.get("profile_moderation_status", "N/A"),
            "notes": onboarding_data.get("notes", []),
        }
    else:
        summary = {
            "user_id": user_id,
            "status": "not_found",
            "message": "Onboarding data not found for this user.",
        }
        
    return summary
