import os
from google.cloud import speech
from google.cloud import translate_v2 as translate
from google.generativeai import client as genai_client
from google.api_core.client_options import ClientOptions


def get_speech_client():
    return speech.SpeechClient()


def get_async_speech_client():
    return speech.SpeechAsyncClient()


def get_translation_client():
    return translate.Client()


def get_generative_client():
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai_client.configure(api_key=api_key)
    return genai_client


def get_perspective_client_config():
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")

    return {
        "discoveryServiceUrl": f"https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1&key={api_key}",
        "developerKey": api_key,
    }
