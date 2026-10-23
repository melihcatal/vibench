import os
from document_models import TextExtractionResult, TranslationResult
from google.cloud import translate


def translate_text(
    text_to_translate: TextExtractionResult, target_language: str, project_id: str
) -> TranslationResult:
    client = translate.TranslationServiceClient()

    # The project ID and target language are required.
    # Location is optional, but recommended for latency.
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text_to_translate.text],
            "target_language_code": target_language,
        }
    )

    translated_text_output = ""
    source_language_output = ""
    for translation in response.translations:
        translated_text_output = translation.translated_text
        source_language_output = translation.detected_language_code

    return TranslationResult(
        translated_text=translated_text_output,
        source_language=source_language_output,
        target_language=target_language,
    )


if __name__ == "main":
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    TARGET_LANG = "es"  # Example target language

    if not PROJECT_ID:
        print("Please set GOOGLE_CLOUD_PROJECT_ID environment variable.")
    else:
        sample_text = TextExtractionResult(
            text="Hello, this is a sample text to be translated."
        )
        translation_result = translate_text(sample_text, TARGET_LANG, PROJECT_ID)
        print(f"Original Text: {sample_text.text}")
        print(
            f"Translated Text ({translation_result.target_language} from {translation_result.source_language}): {translation_result.translated_text}"
        )
