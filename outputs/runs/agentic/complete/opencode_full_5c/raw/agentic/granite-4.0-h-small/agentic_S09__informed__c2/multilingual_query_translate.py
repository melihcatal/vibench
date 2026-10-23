import os
import requests
from typing import List

# Example: using Alibaba Machine Translation SDK
# Requires ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET environment variables

API_ENDPOINT = os.getenv(
    "ALIBABA_ALIMT_ENDPOINT", "https://mt.cn-shanghai.aliyuncs.com"
)

headers = {"Content-Type": "application/x-www-form-urlencoded"}


def translate_text(texts: List[str], target_lang: str = "en") -> List[str]:
    """Translate a list of query strings to the target language using Alibaba Machine Translation.

    Args:
        texts (List[str]): List of query strings to translate.
        target_lang (str): ISO language code for target language (default 'en').

    Returns:
        List[str]: Translated query strings.
    """
    payload = {
        "Action": "TranslateText",
        "Version": "2020-06-01",
        "SourceLanguage": "auto",
        "TargetLanguage": target_lang,
        "Text": "\n".join(texts),  # Alibaba expects \n separated text
    }
    response = requests.post(API_ENDPOINT, headers=headers, data=payload)
    response.raise_for_status()
    data = response.json()
    # Alibaba returns a list of translated texts in 'Translated' field
    translations = data.get("Translated", [])
    return [t.strip() for t in translations]
