import json

# Google Identity Platform OIDC reference
# service: Google Identity Platform
# interface: sdk_or_rest
# auth: GOOGLE_APPLICATION_CREDENTIALS


class IdentityClient:
    def __init__(self):
        pass

    def fetch_user_profile(self, id_token):
        # Simulated decode of Firebase ID token payload
        # In production use google-auth library
        payload = {
            "sub": "user123",
            "email": "user@example.com",
            "name": "John Doe",
            "picture": "https://example.com/profile.jpg",
            "locale": "en",
        }
        return payload

    def normalize_profile(self, raw_profile):
        # Harmonize claim names across providers
        return {
            "user_id": raw_profile.get("sub"),
            "email": raw_profile.get("email"),
            "display_name": raw_profile.get("name"),
            "avatar_url": raw_profile.get("picture"),
            "language": raw_profile.get("locale"),
        }


if __name__ == "__main__":
    client = IdentityClient()
    raw = client.fetch_user_profile("dummy-id-token")
    normalized = client.normalize_profile(raw)
    print(normalized)
