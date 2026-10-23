import json
from identity_client import IdentityClient

# Providers for profile normalization
PROVIDERS = {
    "microsoft": "https://graph.microsoft.com/v1.0/me",
    "google": "https://www.googleapis.com/oauth2/v3/userinfo",
    "alibaba": "https://account.aliyun.com/api/userinfo",
    "auth0": "https://{domain}/userinfo",
    # add others as needed
}


def fetch_profile(provider_name, token):
    provider = PROVIDERS.get(provider_name.lower())
    if not provider:
        raise ValueError(f"{provider_name} not supported")
    # Simple GET request (replace with IdentityClient if needed)
    import requests

    headers = {"Authorization": f"Bearer {token}"}
    resp = requests.get(provider, headers=headers)
    resp.raise_for_status()
    return resp.json()


def normalize_profile(raw_profile, provider_name):
    # Normalize to a common format: email, name, sub, picture
    lower = provider_name.lower()
    user = {"provider": lower}
    if lower == "microsoft":
        user["email"] = raw_profile.get("mail") or raw_profile.get("userPrincipalName")
        user["name"] = raw_profile.get("displayName")
        user["sub"] = raw_profile.get("id")
        user["picture"] = raw_profile.get("photo") or raw_profile.get("thumbnailPhoto")
    elif lower == "google":
        user["email"] = raw_profile.get("email")
        user["name"] = raw_profile.get("name")
        user["sub"] = raw_profile.get("sub")
        user["picture"] = raw_profile.get("picture")
    elif lower == "alibaba":
        user["email"] = raw_profile.get("email")
        user["name"] = raw_profile.get("nickName")
        user["sub"] = raw_profile.get("userId")
        user["picture"] = raw_profile.get("avatarUrl")
    elif lower == "auth0":
        user["email"] = raw_profile.get("email")
        user["name"] = raw_profile.get("name")
        user["sub"] = raw_profile.get("sub")
        user["picture"] = raw_profile.get("picture")
    else:
        raise ValueError(f"Unsupported provider {provider_name}")
    return user


# Example usage (run locally)
if __name__ == "__main__":
    import os

    provider = os.getenv("PROFILE_PROVIDER", "microsoft")
    token = os.getenv("PROFILE_TOKEN")
    if provider and token:
        raw = fetch_profile(provider, token)
        profile = normalize_profile(raw, provider)
        print(json.dumps(profile, indent=2))
    else:
        print("Set PROFILE_PROVIDER and PROFILE_TOKEN env vars to test")
