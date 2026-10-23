import json

def onboarding_summary(user_id: str, registration_data: dict, profile: dict, notes: str) -> str:
    """Create a concise support summary of the onboarding state.

    Constructs a JSON‑formatted summary that includes user ID, creation timestamp,
    locale, profile metadata (status, moderation result), and optional onboarding notes.
    """
    summary = {
        'user_id': user_id,
        'created_at': registration_data['created_at'],
        'locale': registration_data.get('locale', 'en'),
        'profile': {
            'status': profile.get('status', 'pending'),
            'moderation': profile.get('moderation_status', 'clear')
        },
        'notes': notes or ''
    }
    return json.dumps(summary, indent=2)
