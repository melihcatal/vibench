import os
from openai import OpenAI
from google.cloud import speech
import boto3

class SpeechClientConfig:
    """
    Configuration class for various speech-to-text clients.
    """
    def __init__(self):
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.aws_region = os.getenv("AWS_REGION", "us-east-1")
        # Google Cloud credentials are typically handled by GOOGLE_APPLICATION_CREDENTIALS
        # environment variable or automatically by the client library.

class SpeechClients:
    """
    Provides initialized client instances for different speech-to-text services.
    """
    def __init__(self, config: SpeechClientConfig):
        self.config = config

    def get_openai_client(self):
        if not self.config.openai_api_key:
            raise ValueError("OpenAI API key not configured.")
        return OpenAI(api_key=self.config.openai_api_key)

    def get_google_speech_client(self):
        return speech.SpeechAsyncClient()

    def get_aws_transcribe_client(self):
        return boto3.client('transcribe', region_name=self.config.aws_region)


# Example usage (for testing or direct instantiation)
if __name__ == "__main__":
    # Ensure relevant environment variables are set for this example to work fully
    # export OPENAI_API_KEY="your_openai_key"
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/google_credentials.json"
    # export AWS_ACCESS_KEY_ID="your_aws_access_key_id"
    # export AWS_SECRET_ACCESS_KEY="your_aws_secret_access_key"
    # export AWS_REGION="us-east-1"

    config = SpeechClientConfig()
    clients = SpeechClients(config)

    try:
        openai_client = clients.get_openai_client()
        print("OpenAI client initialized.")
    except ValueError as e:
        print(f"OpenAI client not initialized: {e}")

    try:
        google_client = clients.get_google_speech_client()
        print("Google Speech client initialized.")
    except Exception as e:
        print(f"Google Speech client not initialized: {e}")

    try:
        aws_client = clients.get_aws_transcribe_client()
        print("AWS Transcribe client initialized.")
    except Exception as e:
        print(f"AWS Transcribe client not initialized: {e}")
