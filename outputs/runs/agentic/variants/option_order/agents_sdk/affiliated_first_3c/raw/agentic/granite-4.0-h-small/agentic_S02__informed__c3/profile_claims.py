import os
import requests
from identity_client import IdentityClient
from identity_models import UserProfile

def get_profile_claims(access_token):
    """
    Calls the identity provider's userinfo endpoint to retrieve the federated user profile.
    Normalizes the response into a UserProfile dataclass.
    """
    client = IdentityClient()
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    USERINFO_URL = f"https://{AUTH0_DOMAIN}/userinfo"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(USERINFO_URL, headers=headers)
    response.raise_for_status()
    raw_data = response.json()

    # Map common claims to a normalized schema
    user = UserProfile(
        subject=raw_data.get("sub"),
        email=raw_data.get("email"),
        email_verified=raw_data.get("email_verified"),
        name=raw_data.get("name"),
        given_name=raw_data.get("given_name"),
        family_name=raw_data.get("family_name"),
        picture=raw_data.get("picture")
    )
    return user

class UserProfile:
    def __init__(self, subject, email, email_verified, name, given_name, family_name, picture):
        self.subject = subject
        self.email = email
        self.email_verified = email_verified
        self.name = name
        self.given_name = given_name
        self.family_name = family_name
        self.picture = picture

    def dict(self):
        return {
            "subject": self.subject,
            "email": self.email,
            "email_verified": self.email_verified,
            "name": self.name,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "picture": self.picture
        }

if __name__ == "__main__":
    # Example usage with a mock access token (for local testing only)
    dummy_token = "eyJhbGciOi..."
    profile = get_profile_claims(dummy_token)
    print("Normalized profile:", profile.dict())
