import os

import cohere
import elevenlabs
import openai
import vertexai
from google.cloud import translate_v2 as translate
from googleapiclient import discovery


def get_cohere_client():
    """Initializes and returns a Cohere client."""
    api_key = os.environ.get("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable not set.")
    return cohere.Client(api_key)

def initialize_vertexai():
    """Initializes Vertex AI with project and location from environment."""
    project = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION")
    if not project or not location:
        raise ValueError("GOOGLE_CLOUD_PROJECT and GOOGLE_CLOUD_LOCATION must be set.")
    vertexai.init(project=project, location=location)

def get_openai_client():
    """Initializes and returns an OpenAI client."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return openai.OpenAI(api_key=api_key)

def get_google_translate_client():
    """Initializes and returns a Google Translate client."""
    return translate.Client()

def get_perspective_client():
    """Initializes and returns a Perspective API client."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY for Perspective API must be set.")
    return discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )

def get_elevenlabs_client():
    """Initializes and returns an ElevenLabs client."""
    api_key = os.environ.get("ELEVEN_LABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVEN_LABS_API_KEY environment variable not set.")
    return elevenlabs.client.ElevenLabs(api_key=api_key)
