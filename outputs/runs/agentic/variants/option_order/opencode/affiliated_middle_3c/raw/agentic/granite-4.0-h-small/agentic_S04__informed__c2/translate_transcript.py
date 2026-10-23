import os
from typing import Dict, List, Tuple
from pathlib import Path

# Translation utilities using Alibaba Cloud Machine Translation API

ALIBABA_ACCESS_KEY_ID = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
ALIBABA_ACCESS_KEY_SECRET = os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
if not ALIBABA_ACCESS_KEY_ID or not ALIBABA_ACCESS_KEY_SECRET:
    raise RuntimeError(
        "ALIBABA_CLOUD_ACCESS_KEY_ID or ALIBABA_CLOUD_ACCESS_KEY_SECRET not set"
    )

BASE_URL = "https://mt.cn-hangzhou.aliyuncs.com"

from requests import Session, HTTPError

session = Session()
session.headers.update({"Content-Type": "application/json"})

# Simple request wrapper for Alibaba MT API


def translate_segments(segments: List[str], target_lang: str = "en") -> List[str]:
    payload = {
        "SourceText": "\n".join(segments),
        "SourceLanguage": "auto",
        "TargetLanguage": target_lang,
        "FormatType": "text",
    }
    resp = session.post(
        f"{BASE_URL}/api/translate",
        json=payload,
        auth=(ALIBABA_ACCESS_KEY_ID, ALIBABA_ACCESS_KEY_SECRET),
    )
    resp.raise_for_status()
    result = resp.json()
    return result.get("TranslatedText", "").split("\n")


# Example usage (not executed during file creation)
# translated = translate_segments(['Bonjour', 'Comment ça va?'], target_lang='en')
# print(translated)
