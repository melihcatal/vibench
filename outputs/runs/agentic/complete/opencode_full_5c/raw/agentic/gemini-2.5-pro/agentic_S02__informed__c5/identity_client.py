import os
from dotenv import load_dotenv

load_dotenv()


class IdentityClient:
    # Auth0 Configuration
    AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
    AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
    AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")
    AUTH0_CALLBACK_URL = "http://localhost:3000/callback"

    # AWS Configuration for DynamoDB and Translate
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION_NAME = os.getenv("AWS_REGION_NAME", "us-east-1")
    DYNAMODB_TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME", "federated-logins")

    # Google Gemini Configuration
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # Azure Content Safety Configuration
    AZURE_CONTENT_SAFETY_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    AZURE_CONTENT_SAFETY_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")

    # DeepL Configuration
    DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")

    @staticmethod
    def get_auth0_config():
        return {
            "domain": IdentityClient.AUTH0_DOMAIN,
            "client_id": IdentityClient.AUTH0_CLIENT_ID,
            "client_secret": IdentityClient.AUTH0_CLIENT_SECRET,
            "redirect_uri": IdentityClient.AUTH0_CALLBACK_URL,
        }


identity_client = IdentityClient()
