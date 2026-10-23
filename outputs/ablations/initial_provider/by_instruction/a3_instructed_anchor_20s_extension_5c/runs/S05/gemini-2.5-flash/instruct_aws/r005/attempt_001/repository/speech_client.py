import os
import boto3
from google.cloud import speech_v1p1beta1 as speech
from google.cloud import translate_v3 as translate
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety import ContentSafetyClient
from openai import OpenAI
import cohere

class AWSConfig:
    AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
    AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")

class GoogleCloudConfig:
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") # Path to service account key file

class AzureConfig:
    AZURE_CONTENT_SAFETY_ENDPOINT = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    AZURE_CONTENT_SAFETY_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

class OpenAIConfig:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

class CohereConfig:
    COHERE_API_KEY = os.environ.get("COHERE_API_KEY")

class SpeechClient:
    def __init__(self):
        # AWS Transcribe Client
        self.aws_transcribe_client = boto3.client(
            "transcribe",
            region_name=AWSConfig.AWS_REGION,
            aws_access_key_id=AWSConfig.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWSConfig.AWS_SECRET_ACCESS_KEY
        )

        # Google Cloud Speech-to-Text Client
        # GOOGLE_APPLICATION_CREDENTIALS environment variable is typically used for authentication
        self.google_speech_client = speech.SpeechClient()

        # Google Cloud Translation Client
        self.google_translate_client = translate.TranslationServiceClient()

        # Azure Content Safety Client
        self.azure_content_safety_client = None
        if AzureConfig.AZURE_CONTENT_SAFETY_ENDPOINT and AzureConfig.AZURE_CONTENT_SAFETY_KEY:
            self.azure_content_safety_client = ContentSafetyClient(
                endpoint=AzureConfig.AZURE_CONTENT_SAFETY_ENDPOINT,
                credential=AzureKeyCredential(AzureConfig.AZURE_CONTENT_SAFETY_KEY)
            )
        
        # OpenAI Client
        self.openai_client = OpenAI(api_key=OpenAIConfig.OPENAI_API_KEY)

        # Cohere Client
        self.cohere_client = cohere.Client(api_key=CohereConfig.COHERE_API_KEY)

    def get_aws_transcribe_client(self):
        return self.aws_transcribe_client

    def get_google_speech_client(self):
        return self.google_speech_client

    def get_google_translate_client(self):
        return self.google_translate_client
    
    def get_azure_content_safety_client(self):
        return self.azure_content_safety_client

    def get_openai_client(self):
        return self.openai_client

    def get_cohere_client(self):
        return self.cohere_client

