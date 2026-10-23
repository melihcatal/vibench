import os
import requests
import json

def fetch_google_profile_claims(access_token: str):
    """Fetches user profile claims from Google People API."""
    profile_url = "https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses,photos"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    try:
        response = requests.get(profile_url, headers=headers)
        response.raise_for_status()
        profile_data = response.json()
        return profile_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching profile claims: {e}")
        return None

def normalize_google_profile(profile_data: dict):
    """Normalizes the Google People API response into a standard format."""
    normalized_profile = {
        "provider": "google",
        "id": profile_data.get("resourceName", "").split('/')[-1] if "resourceName" in profile_data else None,
        "display_name": None,
        "email": None,
        "picture": None,
    }

    if "names" in profile_data and profile_data["names"]:
        for name in profile_data["names"]:
            if name.get("metadata", {}).get("primary"):
                normalized_profile["display_name"] = name.get("displayName")
                break
        if not normalized_profile["display_name"] and profile_data["names"]:
             normalized_profile["display_name"] = profile_data["names"][0].get("displayName")

    if "emailAddresses" in profile_data and profile_data["emailAddresses"]:
        for email in profile_data["emailAddresses"]:
            if email.get("metadata", {}).get("primary"):
                normalized_profile["email"] = email.get("value")
                break
        if not normalized_profile["email"] and profile_data["emailAddresses"]:
            normalized_profile["email"] = profile_data["emailAddresses"][0].get("value")

    if "photos" in profile_data and profile_data["photos"]:
        for photo in profile_data["photos"]:
            if photo.get("metadata", {}).get("primary"):
                normalized_profile["picture"] = photo.get("url")
                break
        if not normalized_profile["picture"] and profile_data["photos"]:
            normalized_profile["picture"] = profile_data["photos"][0].get("url")

    return normalized_profile

if __name__ == "__main__":
    # This part simulates having an access token
    # In a real application, this would come from the oauth_callback.py step
    example_access_token = os.environ.get("GOOGLE_ACCESS_TOKEN", "_YOUR_SIMULATED_ACCESS_TOKEN_")

    if example_access_token == "_YOUR_SIMULATED_ACCESS_TOKEN_":
        print("Please set GOOGLE_ACCESS_TOKEN environment variable or replace the placeholder.")
    else:
        print("Fetching profile claims with simulated access token...")
        profile_raw = fetch_google_profile_claims(example_access_token)

        if profile_raw:
            print("\nRaw Google Profile Data:")
            print(json.dumps(profile_raw, indent=2))
            
            normalized_profile = normalize_google_profile(profile_raw)
            print("\nNormalized Profile Claims:")
            print(json.dumps(normalized_profile, indent=2))
        else:
            print("Failed to fetch profile claims.")
