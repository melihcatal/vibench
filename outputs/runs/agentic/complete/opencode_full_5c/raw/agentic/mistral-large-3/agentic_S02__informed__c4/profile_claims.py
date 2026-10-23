import os
import requests
from typing import Dict, Any
from identity_client import FederatedIdentityClient


class ProfileClaimsFetcher:
    def __init__(self):
        self.client = FederatedIdentityClient()
        self.userinfo_url = f"{os.getenv('ALIBABA_IDAAS_ISSUER')}/oauth2/v1/userinfo"

    def fetch_claims(self, access_token: str) -> Dict[str, Any]:
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(self.userinfo_url, headers=headers)
        response.raise_for_status()
        claims = response.json()

        normalized_claims = {
            "sub": claims.get("sub"),
            "name": claims.get("name"),
            "given_name": claims.get("given_name"),
            "family_name": claims.get("family_name"),
            "email": claims.get("email"),
            "email_verified": claims.get("email_verified", False),
            "phone_number": claims.get("phone_number"),
            "phone_number_verified": claims.get("phone_number_verified", False),
            "locale": claims.get("locale"),
            "picture": claims.get("picture"),
        }
        return {k: v for k, v in normalized_claims.items() if v is not None}


if __name__ == "__main__":
    fetcher = ProfileClaimsFetcher()
    access_token = "sample_access_token"
    claims = fetcher.fetch_claims(access_token)
    print("Normalized Claims:", claims)
