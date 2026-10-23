import os
from google.cloud import logging as gc_logging
from google.cloud import translate_v3 as gc_translate
import openai

def get_logging_client():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    return gc_logging.Client(project=project_id)

def get_openai_client():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")
    return openai.OpenAI(api_key=api_key)

def get_translation_client():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID") 
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    return gc_translate.TranslationServiceClient()
