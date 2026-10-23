import os
from google.cloud import translate_v3 as translate
from typing import Dict, Any


def translate_consent_copy(
    text: str, target_language_code: str, project_id: str
) -> Dict[str, Any]:
    """
    Translates identity-provider consent copy using Google Cloud Translation API.

    Args:
        text: The consent text to translate.
        target_language_code: The BCP-47 language code of the target language (e.g., "es" for Spanish).
        project_id: The Google Cloud project ID.

    Returns:
        A dictionary containing the original text, translated text, and target language.
    """
    client = translate.TranslationServiceClient()

    location = "global"  # For general purpose translation
    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
            "target_language_code": target_language_code,
        }
    )

    translated_text = ""
    if response.translations:
        translated_text = response.translations[0].translated_text

    translation_result = {
        "original_text": text,
        "translated_text": translated_text,
        "target_language": target_language_code,
        "provider": "Google Cloud Translation API",
    }
    return translation_result


if __name__ == "__main__":
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    if project_id == "your-gcp-project-id":
        print(
            "Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id'."
        )
    else:
        example_consent_text = "By clicking 'Accept', you agree to our terms and conditions and privacy policy."
        target_lang = "es"
        translation_output = translate_consent_copy(
            example_consent_text, target_lang, project_id
        )
        import json

        print(json.dumps(translation_output, indent=2))

        example_consent_text_jp = "このサービスを使用することにより、利用規約とプライバシーポリシーに同意するものとします。"
        target_lang_en = "en"
        translation_output_en = translate_consent_copy(
            example_consent_text_jp, target_lang_en, project_id
        )
        print("\n--- Japanese to English Translation ---")
        print(json.dumps(translation_output_en, indent=2))
