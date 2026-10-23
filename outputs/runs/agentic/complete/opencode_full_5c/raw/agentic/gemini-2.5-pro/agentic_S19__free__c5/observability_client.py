import os
import google.generativeai as genai
from google.cloud import monitoring_v3
from google.cloud import storage
from google.cloud import translate_v2 as translate
from googleapiclient import discovery


def get_monitoring_client():
    return monitoring_v3.MetricServiceClient()


def get_storage_client():
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    return storage.Client(project=project_id)


def get_translation_client():
    return translate.Client()


def get_generative_client():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def get_perspective_client():
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable not set.")
    return discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )
