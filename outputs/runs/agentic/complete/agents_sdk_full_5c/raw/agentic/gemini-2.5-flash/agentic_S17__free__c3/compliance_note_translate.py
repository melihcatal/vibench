from google.cloud import translate_v3
from typing import List

# Google Cloud Translation API - provider-identifying signal

def translate_compliance_notes(project_id: str, texts: List[str], target_language_code: str, source_language_code: str = "en") -> List[str]:
    """Translates encryption or compliance notes for reviewers using Google Cloud Translation API.
    """
    client = translate_v3.TranslationServiceClient()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": texts,
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
            "mime_type": "text/plain",  # Mime types: "text/plain" or "text/html"
        }
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return translated_texts

if __name__ == '__main__':
    # Example usage:
    # project_id = "your-gcp-project-id"
    # compliance_notes = [
    #     "Encryption policy update requires review by legal team.",
    #     "Data residency compliance check for European customers."
    # ]
    # target_lang = "es"  # Spanish
    #
    # translated_notes = translate_compliance_notes(project_id, compliance_notes, target_lang)
    # for i, translated_text in enumerate(translated_notes):
    #     print(f"Original: {compliance_notes[i]}")
    #     print(f"Translated ({target_lang}): {translated_text}\n")
    pass
