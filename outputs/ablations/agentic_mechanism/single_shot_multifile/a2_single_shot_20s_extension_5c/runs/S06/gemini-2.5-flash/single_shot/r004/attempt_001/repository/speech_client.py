import os
import boto3
from google.cloud import texttospeech, speech
import azure.cognitiveservices.speech as speech_sdk
import openai
import cohere
import requests

def get_google_tts_client():
    return texttospeech.TextToSpeechClient()

def get_google_stt_client():
    return speech.SpeechClient()

def get_aws_polly_client():
    return boto3.client("polly")

def get_aws_s3_client():
    return boto3.client("s3")

def get_azure_speech_config():
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    service_region = os.getenv("AZURE_SPEECH_REGION")
    if not speech_key or not service_region:
        raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables must be set for Azure Speech.")
    return speech_sdk.SpeechConfig(subscription=speech_key, region=service_region)

def get_openai_client():
    if not os.getenv("OPENAI_API_KEY"):
        raise ValueError("OPENAI_API_KEY environment variable must be set.")
    return openai.OpenAI()

def get_cohere_client():
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable must be set.")
    return cohere.Client(api_key=api_key)

def get_deepl_api_key():
    api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable must be set.")
    return api_key
