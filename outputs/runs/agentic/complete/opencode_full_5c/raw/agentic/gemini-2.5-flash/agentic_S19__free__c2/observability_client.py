import os
from google.cloud import monitoring_v3
from google.cloud import translate_v3
from google.cloud import storage
from google.cloud import language_v1


def get_monitoring_client():
    return monitoring_v3.MetricServiceClient()


def get_translation_client():
    return translate_v3.TranslationServiceClient()


def get_storage_client():
    return storage.Client()


def get_language_client():
    return language_v1.LanguageServiceClient()


def get_project_id():
    # Replace with your Google Cloud Project ID
    return os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
