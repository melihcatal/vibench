import os
from google.cloud import vision
from google.cloud import translate_v2 as translate
from google.cloud import storage
import vertexai
import openai


def get_vision_client():
    return vision.ImageAnnotatorClient()


def get_translate_client():
    return translate.Client()


def get_storage_client():
    return storage.Client()


defconfigure_vertexai():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "us-central1")
    if project_id:
        vertexai.init(project=project_id, location=location)

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    return openai.OpenAI(api_key=api_key)

configure_vertexai()
