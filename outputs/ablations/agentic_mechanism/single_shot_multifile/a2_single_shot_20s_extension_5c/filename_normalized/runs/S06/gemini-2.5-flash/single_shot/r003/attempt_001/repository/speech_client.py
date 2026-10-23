import os

class SpeechClientConfig:
    def __init__(self):
        self.aws_region = os.environ.get('AWS_REGION', 'us-east-1')
        self.aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY')

        self.google_credential_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

        self.azure_speech_key = os.environ.get('AZURE_SPEECH_KEY')
        self.azure_speech_region = os.environ.get('AZURE_SPEECH_REGION', 'eastus')

        self.deepl_auth_key = os.environ.get('DEEPL_AUTH_KEY')
        self.openai_api_key = os.environ.get('OPENAI_API_KEY')
        self.cohere_api_key = os.environ.get('COHERE_API_KEY')
        self.assemblyai_api_key = os.environ.get('ASSEMBLYAI_API_KEY')

class SpeechClient:
    def __init__(self):
        self.config = SpeechClientConfig()

    def get_aws_region(self) -> str:
        return self.config.aws_region

    def get_deepl_auth_key(self) -> str:
        return self.config.deepl_auth_key
