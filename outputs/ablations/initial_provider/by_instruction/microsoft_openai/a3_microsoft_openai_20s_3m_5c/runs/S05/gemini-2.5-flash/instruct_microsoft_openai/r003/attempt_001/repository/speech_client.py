import os
from typing import Dict, Any

class SpeechClientConfig:
    """Manages configuration settings for various speech-to-text providers."""
    def __init__(self):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        self.google_credentials_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        self.aws_region = os.environ.get("AWS_REGION")
        self.aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
        self.aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
        self.ibm_watson_apikey = os.environ.get("IBM_WATSON_SPEECH_TO_TEXT_APIKEY")
        self.ibm_watson_url = os.environ.get("IBM_WATSON_SPEECH_TO_TEXT_URL")

    def get_openai_config(self) -> Dict[str, Any]:
        return {"api_key": self.openai_api_key}

    def get_google_config(self) -> Dict[str, Any]:
        return {"credentials_path": self.google_credentials_path}

    def get_aws_config(self) -> Dict[str, Any]:
        return {
            "region_name": self.aws_region,
            "aws_access_key_id": self.aws_access_key_id,
            "aws_secret_access_key": self.aws_secret_access_key,
        }

    def get_ibm_watson_config(self) -> Dict[str, Any]:
        return {
            "apikey": self.ibm_watson_apikey,
            "url": self.ibm_watson_url
        }

class SpeechClientFactory:
    """Provides methods to create configured client instances for speech-to-text providers."""
    def __init__(self, config: SpeechClientConfig):
        self._config = config

    def get_openai_client(self):
        """Returns an OpenAI client instance."""
        import openai
        return openai.OpenAI(api_key=self._config.openai_api_key)

    def get_google_client(self):
        """Returns a Google Cloud Speech client instance."""
        from google.cloud import speech
        # Google Cloud client typically uses GOOGLE_APPLICATION_CREDENTIALS implicitly
        # or can be explicitly configured.
        return speech.SpeechClient()

    def get_aws_client_session(self):
        """Returns a boto3 session configured for AWS."""
        import boto3
        return boto3.Session(
            region_name=self._config.aws_region,
            aws_access_key_id=self._config.aws_access_key_id,
            aws_secret_access_key=self._config.aws_secret_access_key
        )

    def get_ibm_watson_client(self):
        """Returns an IBM Watson SpeechToTextV1 client instance."""
        from ibm_watson import SpeechToTextV1
        from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
        authenticator = IAMAuthenticator(self._config.ibm_watson_apikey)
        service = SpeechToTextV1(authenticator=authenticator)
        service.set_service_url(self._config.ibm_watson_url)
        return service

# Example Usage (not part of the file's core functionality, but for context)
if __name__ == "__main__":
    config = SpeechClientConfig()
    factory = SpeechClientFactory(config)

    # Example: Get an OpenAI client
    # openai_client = factory.get_openai_client()
    # print(f"OpenAI client created: {openai_client is not None}")

    # Example: Get a Google Cloud client
    # google_client = factory.get_google_client()
    # print(f"Google Cloud client created: {google_client is not None}")

    # Example: Get an AWS boto3 session
    # aws_session = factory.get_aws_client_session()
    # print(f"AWS session created: {aws_session is not None}")

    # Example: Get an IBM Watson client
    # ibm_client = factory.get_ibm_watson_client()
    # print(f"IBM Watson client created: {ibm_client is not None}")
