def normalize_profile_claims(profile):
    normalized = {
        'user_id': profile['localId'],
        'email': profile['email'],
        'display_name': profile.get('displayName', ''),
        'photo_url': profile.get('photoUrl', '')
    }
    return normalized