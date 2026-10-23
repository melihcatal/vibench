import os
from google.cloud import translate_v3 as translate


def translate_log_message_with_cloud_translation(
    project_id: str, text: str, target_language: str, source_language: str = "en"
) -> str:
    """
    Translates support-visible log messages for another locale using Google Cloud Translation.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    translations = [t.translated_text for t in response.translations]
    translated_text = " ".join(translations)
    print(
        f"Translated '{text}' from {source_language} to {target_language}: '{translated_text}'"
    )
    return translated_text


if __name__ == "__main__":
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")

    log_message_en = (
        "Failed to connect to the database. Please check network connectivity."
    )

    print("Translating to Spanish:")
    translated_es = translate_log_message_with_cloud_translation(
        PROJECT_ID, log_message_en, "es"
    )

    print("\nTranslating to French:")
    translated_fr = translate_log_message_with_cloud_translation(
        PROJECT_ID, log_message_en, "fr"
    )

    log_message_ja = "データベースへの接続に失敗しました。"
    print("\nTranslating Japanese to English:")
    translated_en_from_ja = translate_log_message_with_cloud_translation(
        PROJECT_ID, log_message_ja, "en", source_language="ja"
    )
