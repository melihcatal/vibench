import os
from openai import OpenAI
import azure.cognitiveservices.speech as speechsdk
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from google.cloud import translate_v2 as translate
from google.cloud import speech

class OpenAIClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OpenAIClient, cls).__new__(cls)
            cls._instance.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        return cls._instance.client

class AzureSpeechClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AzureSpeechClient, cls).__new__(cls)
            speech_key = os.environ.get("AZURE_SPEECH_KEY")
            service_region = os.environ.get("AZURE_SPEECH_REGION")
            cls._instance.speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
        return cls._instance.speech_config

class AzureContentSafetyClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AzureContentSafetyClient, cls).__new__(cls)
            endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
            key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
            cls._instance.client = ContentSafetyClient(endpoint, AzureKeyCredential(key))
        return cls._instance.client

class GoogleTranslateClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GoogleTranslateClient, cls).__new__(cls)
            cls._instance.client = translate.Client()
        return cls._instance.client

class GoogleSpeechClient:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GoogleSpeechClient, cls).__new__(cls)
            cls._instance.client = speech.SpeechClient()
        return cls._instance.client

