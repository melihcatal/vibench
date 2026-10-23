from typing import List
from google.cloud import translate_v2 as translate
import os

def translate_log_messages(messages: List[str], target_language: str) -> List[str]:
    client = translate.Client.from_service_account_json(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "credentials.json")
    )
    results = client.translate(
        messages,
        target_language=target_language,
        format_="text"
    )
    return [result["translatedText"] for result in results]