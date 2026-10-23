import os
import openai
import assemblyai
import cohere
import deepl
import elevenlabs
import vertexai
from google.cloud import aiplatform


def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    return openai.OpenAI(api_key=api_key)


def get_assemblyai_client():
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    assemblyai.settings.api_key = api_key
    return assemblyai


def get_cohere_client():
    api_key = os.environ.get("COHERE_API_KEY")
    return cohere.Client(api_key)


def get_deepl_translator():
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    return deepl.Translator(auth_key)


def get_elevenlabs_client():
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    elevenlabs.set_api_key(api_key)
    return elevenlabs


def get_vertexai_client():
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    vertexai.init(project=project, location=location)
    return vertexai
