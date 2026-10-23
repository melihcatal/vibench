import os
import requests

# Google People API
GOOGLE_PEOPLE_API_URL = "https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses,photos"

def fetch_google_profile_claims(access_token: str):
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(GOOGLE_PEOPLE_API_URL, headers=headers)
    response.raise_for_status() # Raise an exception for HTTP errors
    profile_data = response.json()
    return profile_data

def normalize_google_profile_claims(profile_data: dict):
    # Basic normalization for common claims
    normalized_claims = {
        "id": profile_data.get("resourceName", "").split('/')[-1] if profile_data.get("resourceName") else None,
        "email": None,
        "name": None,
        "given_name": None,
        "family_name": None,
        "picture": None,
    }

    if profile_data.get("emailAddresses"):
        for email_entry in profile_data["emailAddresses"]:
            if email_entry.get("metadata", {}).get("primary"):
                normalized_claims["email"] = email_entry.get("value")
                break
        if not normalized_claims["email"] and profile_data["emailAddresses"]:
             normalized_claims["email"] = profile_data["emailAddresses"][0].get("value")

    if profile_data.get("names"):
        for name_entry in profile_data["names"]:
            if name_entry.get("metadata", {}).get("primary"):
                normalized_claims["name"] = name_entry.get("displayName")
                normalized_claims["given_name"] = name_entry.get("givenName")
                normalized_claims["family_name"] = name_entry.get("familyName")
                break
        if not normalized_claims["name"] and profile_data["names"]:
            normalized_claims["name"] = profile_data["names"][0].get("displayName")
            normalized_claims["given_name"] = profile_data["names"][0].get("givenName")
            normalized_claims["family_name"] = profile_data["names"][0].get("familyName")

    if profile_data.get("photos"):
        for photo_entry in profile_data["photos"]:
            if photo_entry.get("metadata", {}).get("primary"):
                normalized_claims["picture"] = photo_entry.get("url")
                break
        if not normalized_claims["picture"] and profile_data["photos"]:
            normalized_claims["picture"] = profile_data["photos"][0].get("url")

    return normalized_claims

if __name__ == "__main__":
    # This requires a valid access token obtained from the oauth_callback step
    # Replace with a real access token for testing
    example_access_token = os.environ.get("GOOGLE_ACCESS_TOKEN", "YOUR_GOOGLE_ACCESS_TOKEN")

    if example_access_token == "YOUR_GOOGLE_ACCESS_TOKEN":
        print("Please set GOOGLE_ACCESS_TOKEN environment variable with a valid token to run this example.")
    else:
        try:
            profile = fetch_google_profile_claims(example_access_token)
            print("Raw Google Profile Data:")
            import json
            print(json.dumps(profile, indent=2))

            normalized_profile = normalize_google_profile_claims(profile)
            print("\nNormalized Profile Claims:")
            print(json.dumps(normalized_profile, indent=2))
        except requests.exceptions.HTTPError as e:
            print(f"Error fetching profile: {e.response.text}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
