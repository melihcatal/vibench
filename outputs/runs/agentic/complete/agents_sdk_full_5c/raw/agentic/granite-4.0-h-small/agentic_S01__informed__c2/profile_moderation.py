import os
from content_moderation_client import ContentModerationClient
from identity_models import RegisterRequest

def moderate_profile(user_id: str, profile_text: str) -> str:
    """Moderate profile text for a newly registered user before activation."""
    client = ContentModerationClient()
    result = client.check_text(profile_text)
    # Simple policy: replace disallowed terms with asterisks; allow approved text otherwise
    if result.get('violations'):
        moderated = result['filtered']  # sanitized version provided by service
    else:
        moderated = profile_text
    return moderated
