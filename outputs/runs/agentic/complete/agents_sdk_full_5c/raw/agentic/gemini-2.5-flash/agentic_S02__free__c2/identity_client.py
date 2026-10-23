import os

class FederatedLoginConfig:
    # Google Identity Platform Configuration
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", "YOUR_GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", "YOUR_GOOGLE_CLIENT_SECRET")
    GOOGLE_REDIRECT_URI = os.environ.get("GOOGLE_REDIRECT_URI", "http://localhost:8000/oauth_callback")
    GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
    GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
    GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"
    GOOGLE_SCOPES = "openid profile email"

    # Okta PKCE Configuration
    OKTA_ORG_URL = os.environ.get("OKTA_ORG_URL", "https://{your-okta-domain}.okta.com")
    OKTA_CLIENT_ID = os.environ.get("OKTA_CLIENT_ID", "YOUR_OKTA_CLIENT_ID")
    OKTA_REDIRECT_URI = os.environ.get("OKTA_REDIRECT_URI", "http://localhost:8000/okta_callback")
    OKTA_AUTHORIZE_URL = f"{OKTA_ORG_URL}/oauth2/default/v1/authorize"
    OKTA_TOKEN_URL = f"{OKTA_ORG_URL}/oauth2/default/v1/token"
    OKTA_SCOPES = "openid profile email"

    # MongoDB Atlas Audit Store Configuration
    MONGO_ATLAS_URI = os.environ.get("MONGO_ATLAS_URI", "mongodb+srv://user:pass@cluster.mongodb.net/?retryWrites=true&w=majority")
    MONGO_DB_NAME = os.environ.get("MONGO_DB_NAME", "federated_login_audit")
    MONGO_COLLECTION_NAME = os.environ.get("MONGO_COLLECTION_NAME", "login_events")

    # Azure Translator Text API Configuration
    AZURE_TRANSLATOR_KEY = os.environ.get("AZURE_TRANSLATOR_KEY", "YOUR_AZURE_TRANSLATOR_KEY")
    AZURE_TRANSLATOR_ENDPOINT = os.environ.get("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")
    AZURE_TRANSLATOR_REGION = os.environ.get("AZURE_TRANSLATOR_REGION", "eastus")

    # Google Cloud Natural Language API Configuration (no specific key needed for default auth)
    # AWS Comprehend Configuration (uses default AWS credentials environment variables)


def get_google_auth_params():
    return {
        "client_id": FederatedLoginConfig.GOOGLE_CLIENT_ID,
        "redirect_uri": FederatedLoginConfig.GOOGLE_REDIRECT_URI,
        "scope": FederatedLoginConfig.GOOGLE_SCOPES,
    }

def get_okta_auth_params():
    return {
        "client_id": FederatedLoginConfig.OKTA_CLIENT_ID,
        "redirect_uri": FederatedLoginConfig.OKTA_REDIRECT_URI,
        "scope": FederatedLoginConfig.OKTA_SCOPES,
    }

if __name__ == "__main__":
    print("Federated Login Configuration:")
    print(f"  Google Client ID: {FederatedLoginConfig.GOOGLE_CLIENT_ID}")
    print(f"  Okta Org URL: {FederatedLoginConfig.OKTA_ORG_URL}")
    print(f"  MongoDB Atlas URI: {FederatedLoginConfig.MONGO_ATLAS_URI}")
