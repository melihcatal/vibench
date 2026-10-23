import os


class AzureSpeechClient:
    def __init__(self, api_key=None, region=None):
        self.api_key = api_key or os.environ.get('AZURE_SPEECH_KEY')
        self.region = region or os.environ.get('AZURE_SPEECH_REGION', 'eastus')
        if not self.api_key:
            raise ValueError("Azure Speech API key not provided and AZURE_SPEECH_KEY environment variable not set.")
        if not self.region:
            raise ValueError("Azure Speech region not provided and AZURE_SPEECH_REGION environment variable not set.")

    def get_headers(self):
        return {
            'Ocp-Apim-Subscription-Key': self.api_key,
            'Content-Type': 'application/json'
        }

    def get_base_url(self):
        return f"https://{self.region}.api.cognitive.microsoft.com/speechtotext/v3.1"
