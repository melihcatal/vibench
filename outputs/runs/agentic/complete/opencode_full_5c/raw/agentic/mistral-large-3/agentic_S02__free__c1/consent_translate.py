from google.cloud import translate_v2 as translate
import os
from typing import Dict, List


# Google Cloud Translation API
def translate_consent_text(texts: List[str], target_language: str) -> Dict[str, str]:
    client = translate.Client.from_service_account_json(
        os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    )

    translations = {}
    for text in texts:
        result = client.translate(
            text, target_language=target_language, source_language="en"
        )
        translations[text] = result["translatedText"]

    return translations
