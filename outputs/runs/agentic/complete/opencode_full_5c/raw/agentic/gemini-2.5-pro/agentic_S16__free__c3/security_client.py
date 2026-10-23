import os
from google.cloud import secretmanager
from google.cloud import aiplatform
from google.cloud import translate_v2 as translate
from googleapiclient import discovery
import google.generativeai as genai


def get_secret_manager_client():
    return secretmanager.SecretManagerServiceClient()


def get_ai_platform_client():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    aiplatform.init(project=project_id, location="us-central1")
    return aiplatform


def get_translation_client():
    return translate.Client()


def get_perspective_client():
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    return discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )


def get_generative_ai_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    return genai
