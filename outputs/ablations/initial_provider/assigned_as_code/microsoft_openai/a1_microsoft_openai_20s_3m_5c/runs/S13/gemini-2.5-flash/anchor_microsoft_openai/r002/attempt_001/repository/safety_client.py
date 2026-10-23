from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from google.cloud import dlp


class SafetyClient:
    def __init__(self, provider, config):
        self.provider = provider
        self.config = config

    def get_azure_content_safety_client(self):
        if self.provider == 'azure':
            return ContentSafetyClient(self.config['endpoint'], AzureKeyCredential(self.config['api_key']))
        else:
            raise ValueError("Provider is not configured for Azure Content Safety.")

    def get_google_dlp_client(self):
        if self.provider == 'gcp':
            # Google Cloud DLP client typically gets credentials from the environment
            return dlp.DlpServiceClient()
        else:
            raise ValueError("Provider is not configured for Google Cloud DLP.")

    # Add other client getters as needed for other services
