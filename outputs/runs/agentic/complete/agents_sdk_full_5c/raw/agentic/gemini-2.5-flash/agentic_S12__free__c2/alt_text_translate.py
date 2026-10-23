from typing import List, Dict
from google.cloud import translate_v3 as translate
from vision_client import get_translation_client

def translate_alt_text(text: str, target_languages: List[str], project_id: str) -> Dict[str, str]:
    """Translates generated image descriptions to specified target languages."""
    client = get_translation_client()
    parent = f"projects/{project_id}/locations/global"

    translated_texts = {}
    for target_language in target_languages:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [text],
                "target_language_code": target_language,
            }
        )
        for translation in response.translations:
            translated_texts[target_language] = translation.translated_text
    return translated_texts

if __name__ == '__main__':
    # Replace with your actual GCP project ID
    project_id = "your-gcp-project-id"
    description = "A majestic mountain range with a clear blue sky."
    target_langs = ["es", "fr"] # Spanish, French

    translations = translate_alt_text(description, target_langs, project_id)
    print(f"Original: {description}")
    for lang, translated_text in translations.items():
        print(f"Translated ({lang}): {translated_text}")
