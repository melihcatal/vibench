import os
import deepl
from openai import OpenAI
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer

# DeepL Client
deepl_auth_key = os.getenv("DEEPL_AUTH_KEY")
deepl_translator = deepl.Translator(deepl_auth_key) if deepl_auth_key else None

# OpenAI Client for LLM Inference and Embeddings
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_client = OpenAI(api_key=openai_api_key) if openai_api_key else None

# Azure AI Content Safety Client
azure_content_safety_endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
azure_content_safety_key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
azure_content_safety_client = None
if azure_content_safety_endpoint and azure_content_safety_key:
    azure_content_safety_client = ContentSafetyClient(
        endpoint=azure_content_safety_endpoint,
        credential=AzureKeyCredential(azure_content_safety_key),
    )

# Azure AI Speech TTS Client
azure_speech_key = os.getenv("AZURE_SPEECH_KEY")
azure_speech_region = os.getenv("AZURE_SPEECH_REGION")
azure_speech_synthesizer = None
if azure_speech_key and azure_speech_region:
    speech_config = SpeechConfig(
        subscription=azure_speech_key, region=azure_speech_region
    )
    azure_speech_synthesizer = SpeechSynthesizer(speech_config=speech_config)
