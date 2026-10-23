import os

class Auth0Config:
    """
    A simple class to hold Auth0 configuration loaded from environment variables.
    """
    def __init__(self):
        self.domain = os.environ.get("AUTH0_DOMAIN")
        self.client_id = os.environ.get("AUTH0_CLIENT_ID")
        self.client_secret = os.environ.get("AUTH0_CLIENT_SECRET")
        self.callback_url = os.environ.get("AUTH0_CALLBACK_URL", "http://localhost:8000/callback")

    def validate(self):
        if not all([self.domain, self.client_id, self.callback_url]):
            raise ValueError("Missing Auth0_DOMAIN, AUTH0_CLIENT_ID, or AUTH0_CALLBACK_URL.")
        # Client secret is optional for PKCE flows, but required for authorization code flow

def get_auth0_config() -> Auth0Config:
    """
    Returns an instance of Auth0Config with loaded environment variables.
    """
    return Auth0Config()

# Example for other potential clients/configurations, e.g., for later-step providers
class GoogleCloudConfig:
    """
    Configuration for Google Cloud services (e.g., Firestore, Translation, Gemini).
    Assumes GOOGLE_APPLICATION_CREDENTIALS is set for authentication.
    """
    def __init__(self):
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        # GOOGLE_APPLICATION_CREDENTIALS is typically handled by the SDK implicitly

    def validate(self):
        if not self.project_id:
            print("Warning: GOOGLE_CLOUD_PROJECT environment variable not set. Some Google Cloud operations might fail.")

class AzureConfig:
    """
    Configuration for Azure services.
    """
    def __init__(self):
        self.content_safety_endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
        self.content_safety_key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
        self.translator_key = os.environ.get("AZURE_TRANSLATOR_KEY")
        self.translator_region = os.environ.get("AZURE_TRANSLATOR_REGION")

    def validate_content_safety(self):
        if not all([self.content_safety_endpoint, self.content_safety_key]):
            raise ValueError("Missing AZURE_CONTENT_SAFETY_ENDPOINT or AZURE_CONTENT_SAFETY_KEY.")

    def validate_translator(self):
        if not all([self.translator_key, self.translator_region]):
            raise ValueError("Missing AZURE_TRANSLATOR_KEY or AZURE_TRANSLATOR_REGION.")

