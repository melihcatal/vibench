import os
import json

# Google Identity Platform OIDC reference
# service: Google Identity Platform
# interface: sdk_or_rest
# auth: GOOGLE_APPLICATION_CREDENTIALS

API_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


class IdentityClient:
    def __init__(self):
        pass

    def load_config(self):
        # Load JSON configuration if needed
        config_path = os.getenv("CONFIG_PATH", "config.json")
        with open(config_path, "r") as f:
            return json.load(f)

    def fetch_user_profile(self, id_token):
        # Simulate a token exchange endpoint
        token_url = "https://oauth2.googleapis.com/tokeninfo"
        payload = {"id_token": id_token}
        resp = requests.post(token_url, data=payload)
        resp.raise_for_status()
        return resp.json()

    def normalize_profile(self, raw_profile):
        # Map Google claims to a common schema
        return {
            "user_id": raw_profile.get("sub"),
            "email": raw_profile.get("email"),
            "display_name": raw_profile.get("name"),
            "avatar_url": raw_profile.get("picture"),
            "language": raw_profile.get("locale"),
        }
