import json
from typing import Dict, Any

def build_onboarding_summary(user_id: str) -> Dict[str, Any]:
    """Summarize onboarding state for support or admin dashboards.","""    # In a realistic system we would pull from multiple sources:
    # - Identity service (user creation date, status, attributes)
    # - Moderation store (profile text review status)
    # - Translation cache (locale preferences)
    # - Document store (notes, attachments)
    # Here we emulate a summary using dummy data structures.
    summary = {
        'user_id': user_id,
        'created_at': '2025-08-14T12:00:00Z',
        'status': 'PENDING_MODERATION',
        'profile': {
            'locale': 'en',
            'raw_text': 'Sample profile text to be moderated.',
            'moderated_text': '',
            'moderation_status': 'PENDING'
        },
        'translations': {
            'es': 'Texto de perfil en español',
            'fr': 'Texte de profil en français',
            'de': 'Profiltext auf Deutsch'
        },
        'notes': [],
        'metadata': {
            'source_ip': '203.0.113.45',
            'user_agent': 'Mozilla/5.0 (compatible)'
        }
    }
    return summary

# Helper: fetch persisted moderation data (dummy implementation)
def _fetch_moderation(user_id: str) -> Dict[str, Any]:
    # Pretend we loaded from the profile_moderation store
    return {
        'user_id': user_id,
        'raw_text': 'Sample profile text to be moderated.',
        'moderated_text': 'Sample moderated profile text.',
        'moderation_status': 'ACCEPTED'
    }

# Example: produce a summary and persist notes (stub)
def sample_summary() -> None:
    uid = 'user-12345'
    mod_info = _fetch_moderation(uid)
    summary = build_onboarding_summary(uid)
    summary['profile']['moderated_text'] = mod_info['moderated_text']
    summary['profile']['moderation_status'] = mod_info['moderation_status']
    summary['notes'].append({
        'timestamp': '2025-08-14T12:05:00Z',
        'operator': 'support-bot',
        'message': 'Profile moderated successfully.'
    })
    # Persist to a document store here if needed
    print(json.dumps(summary, indent=2))
