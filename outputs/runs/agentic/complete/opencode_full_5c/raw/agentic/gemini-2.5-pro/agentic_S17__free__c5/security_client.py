import os
from google.cloud import kms_v1, logging_v2, translate_v2
import google.generativeai as genai
from google.api_client import discovery


def get_kms_client():
    return kms_v1.KeyManagementServiceClient()


def get_logging_client():
    return logging_v2.LoggingServiceV2Client()


def get_translation_client():
    return translate_v2.Client()


def get_perspective_client():
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    return discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )


def configure_generative_ai():
    api_key = os.environ.get("GENERATIVE_AI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)


def get_project_id():
    return os.environ.get("GOOGLE_CLOUD_PROJECT")


def get_location():
    return os.environ.get("GOOGLE_CLOUD_LOCATION", "global")
