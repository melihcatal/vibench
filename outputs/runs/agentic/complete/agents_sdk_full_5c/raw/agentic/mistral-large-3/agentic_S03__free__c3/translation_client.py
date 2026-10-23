import os
from google.cloud import translate_v3 as translate
from typing import Optional

def get_translation_client() -> translate.TranslationServiceClient:
    """Initialize and return a Google Cloud Translation client."""
    return translate.TranslationServiceClient()

def get_glossary_config(
    glossary_id: Optional[str] = None,
) -> Optional[translate.TranslateTextGlossaryConfig]:
    """Return glossary configuration for Google Cloud Translation."""
    if not glossary_id:
        return None
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
    location = "global"
    return translate.TranslateTextGlossaryConfig(
        glossary=f"projects/{project_id}/locations/{location}/glossaries/{glossary_id}"
    )