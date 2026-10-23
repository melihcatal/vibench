# [LATER-STEP] dashboard_note_translate.py

import os
from .observability_client import get_azure_client
from .observability_models import MetricQueryRequest

# Azure Cognitive Services Translator client
# Requires AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_REGION in environment

try:
    from azure.ai.translation import TranslationClient
    from azure.core.credentials import AzureKeyCredential
    translator = TranslationClient(
        endpoint=os.getenv('AZURE_TRANSLATOR_ENDPOINT'),
        credential=AzureKeyCredential(os.getenv('AZURE_TRANSLATOR_KEY'))
    )
except Exception as e:
    raise RuntimeError("Missing Azure Translator configuration")

SOURCE_LOCALE = 'en'
TARGET_LOCALE = 'es'  # example target language

def translate_dashboard_note(source_text):
    """Translate dashboard or metric note to target locale.",
    if not source_text:
        return ""
    documents = [{"text": source_text}]  # Azure expects a list of dicts
    response = translator.translate(content=documents, to_language=TARGET_LOCALE, from_language=SOURCE_LOCALE)
    translated = response.translations[0].translations[0].text
    return translated

# Example usage (for local testing)
if __name__ == '__main__':
    note = "Instance CPU usage peaked at 95%"
    print(translate_dashboard_note(note))
