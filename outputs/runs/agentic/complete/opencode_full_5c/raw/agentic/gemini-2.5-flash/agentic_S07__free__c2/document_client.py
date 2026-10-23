from google.cloud import (
    vision_v1,
    documentai_v1beta3,
    translate_v3,
    language_v2,
    aiplatform,
)
import os


def get_vision_client():
    return vision_v1.ImageAnnotatorClient()


def get_documentai_client():
    return documentai_v1beta3.DocumentProcessorServiceClient()


def get_translation_client():
    return translate_v3.TranslationServiceClient()


def get_language_client():
    return language_v2.LanguageServiceClient()


def get_aiplatform_client():
    return aiplatform.gapic.PredictionServiceClient()


def get_project_id():
    return os.getenv("GOOGLE_CLOUD_PROJECT_ID")


def get_location():
    return os.getenv("GOOGLE_CLOUD_LOCATION", "us")
