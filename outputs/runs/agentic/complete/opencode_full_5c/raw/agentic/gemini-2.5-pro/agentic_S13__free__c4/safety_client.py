import os
from openai import OpenAI
from googleapiclient import discovery
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from google.cloud import translate_v2 as translate


def get_perspective_client():
    api_key = os.getenv("PERSPECTIVE_API_KEY")
    return discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        static_discovery=False,
    )


def get_azure_content_safety_client():
    endpoint = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
    api_key = os.getenv("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not api_key:
        raise ValueError(
            "Azure Content Safety endpoint and key must be set in environment variables."
        )
    return ContentSafetyClient(endpoint, AzureKeyCredential(api_key))


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    return OpenAI(api_key=api_key)


def get_google_translate_client():
    return translate.Client()
