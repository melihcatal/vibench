import os
from google.cloud import translate

client = translate.TranslationServiceClient()


def translate_query(query: str, target_language: str) -> str:
    parent = client.location_path("your-project-id", "global")
    response = client.translate_text(parent, query, target_language)
    return response.translations[0].translated_text
