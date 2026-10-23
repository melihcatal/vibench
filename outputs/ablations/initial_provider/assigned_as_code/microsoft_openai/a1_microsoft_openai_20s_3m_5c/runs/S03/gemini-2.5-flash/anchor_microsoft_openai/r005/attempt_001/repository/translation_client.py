import os

class AzureTranslatorClient:
    def __init__(self, api_key=None, region=None):
        self.api_key = api_key or os.environ.get("AZURE_TRANSLATOR_API_KEY")
        self.region = region or os.environ.get("AZURE_TRANSLATOR_REGION")
        if not self.api_key or not self.region:
            raise ValueError("Azure Translator API key and region must be provided or set as environment variables.")

    def get_config(self):
        return {
            "api_key": self.api_key,
            "region": self.region
        }
