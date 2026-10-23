from google.cloud import translate_v2 as translate
import os

translate_client = translate.Client.from_service_account_json(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)

def translate_caption(text: str, target_language: str = "es") -> str:
    result = translate_client.translate(
        text,
        target_language=target_language,
        format_="text",
    )
    return result["translatedText"]