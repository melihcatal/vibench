import os
from google.cloud import translate_v2 as translate


def appeal_translate(appeal_text: str, target_language: str = "en") -> str:
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

    if not credentials_path:
        raise ValueError("Google Cloud credentials not configured")

    client = translate.Client.from_service_account_json(credentials_path)

    result = client.translate(
        appeal_text, target_language=target_language, format_="text"
    )

    return result["translatedText"]
