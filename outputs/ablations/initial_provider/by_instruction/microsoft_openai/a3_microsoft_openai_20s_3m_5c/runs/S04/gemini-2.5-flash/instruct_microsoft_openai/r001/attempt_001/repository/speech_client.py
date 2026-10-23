import os
from azure.cognitiveservices.speech import SpeechConfig, SpeechRecognizer, AudioConfig
from azure.storage.blob import BlobServiceClient


class AzureSpeechClient:
    def __init__(self):
        self.speech_key = os.environ.get("AZURE_SPEECH_KEY")
        self.service_region = os.environ.get("AZURE_SPEECH_REGION")
        self.blob_connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")

        if not self.speech_key or not self.service_region:
            raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set.")
        
        self.speech_config = SpeechConfig(subscription=self.speech_key, region=self.service_region)

    def get_blob_service_client(self):
        if not self.blob_connection_string:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable must be set for blob operations.")
        return BlobServiceClient.from_connection_string(self.blob_connection_string)

    def get_speech_config(self):
        return self.speech_config

