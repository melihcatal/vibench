from google.cloud import translate_v2 as translate
import os


def translate_text(
    project_id: str, text: str, target_language: str, source_language: str = None
) -> dict:
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    client = translate.Client(project=project_id)

    result = client.translate(
        text, target_language=target_language, source_language=source_language
    )

    return {
        "translated_text": result["translatedText"],
        "source_language": result["detectedSourceLanguage"]
        if "detectedSourceLanguage" in result
        else source_language,
        "input": result["input"],
    }
