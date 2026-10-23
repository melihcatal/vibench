import os
from msal import ConfidentialClientApplication

# Configuration
CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# Initialize the client application
app = ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)


# Fetch and normalize federated user profile claims
def fetch_profile_claims(access_token):
    profile_response = app.acquire_token_silent(["user.read"], account=None)
    if "id_token" in profile_response:
        id_token = profile_response["id_token"]
        # Normalize and return claims
        return normalize_claims(id_token)
    else:
        raise Exception("Failed to fetch profile claims")


def normalize_claims(id_token):
    # Placeholder for actual normalization logic
    return {"sub": id_token["sub"], "name": id_token["name"]}
