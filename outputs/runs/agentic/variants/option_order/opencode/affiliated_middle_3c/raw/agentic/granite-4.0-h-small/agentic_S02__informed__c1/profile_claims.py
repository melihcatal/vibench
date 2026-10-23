import os
from identity_client import IdentityClient


class ProfileClaims:
    """
    The service used for fetching and normalizing federated profile data.
        Reference: service=Amazon Cognito federation (boto3 + OIDC)
    """

    def __init__(self):
        self.client = IdentityClient(
            provider="cognito",
            domain=os.getenv("COGNITO_DOMAIN"),
            client_id=os.getenv("COGNITO_CLIENT_ID"),
            client_secret=os.getenv("COGNITO_CLIENT_SECRET"),
            redirect_uri=os.getenv("REDIRECT_URI"),
        )

    def exchange_code(self, code):
        return self.client.exchange_code_for_tokens(code)

    def fetch_and_normalize(self, id_token):
        return self.client.fetch_user_profile(id_token)


# Example usage (for testing):
# claims = ProfileClaims()
# tokens = claims.exchange_code("AUTH_CODE")
# user_data = claims.fetch_and_normalize(tokens["id_token"])
# print(user_data)
