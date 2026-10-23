import json
from typing import Dict, Any

class ProfileClaimsNormalizer:
    @staticmethod
    def normalize_profile(raw_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert a provider-specific profile payload to a uniform internal format.
        Expected keys: sub (subject), name, email, picture, locale, etc.
        """
        normalized = {
            'user_id': raw_profile.get('sub'),
            'full_name': raw_profile.get('name'),
            'email': raw_profile.get('email'),
            'picture_url': raw_profile.get('picture'),
            'locale': raw_profile.get('locale')
        }
        return normalized

# Example usage (in a real app this would be called after token exchange)
if __name__ == '__main__':
    sample_auth0 = {
        'sub': 'auth0|1234567890',
        'name': 'Jane Doe',
        'email': 'jane.doe@example.com',
        'picture': 'https://example.com/avatar.jpg',
        'locale': 'en-US'
    }
    print(json.dumps(ProfileClaimsNormalizer.normalize_profile(sample_auth0), indent=2))