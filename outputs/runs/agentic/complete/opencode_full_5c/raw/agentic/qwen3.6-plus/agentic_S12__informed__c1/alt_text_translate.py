import json
import os
import hashlib
import hmac
import base64
import uuid
import datetime
import requests
from typing import Optional
from urllib.parse import quote

ALIBABA_TRANSLATION_ENDPOINT = "https://mt.aliyuncs.com"
ALIBABA_TRANSLATION_API_VERSION = "2018-10-12"
TRANSLATION_ACTION = "TranslateGeneral"
TARGET_SERVICE_VERSION = "2018-10-12"


def _sign_request(
    access_key_secret: str,
    string_to_sign: str,
) -> str:
    """Sign a request using HMAC-SHA1 for Alibaba Cloud API authentication."""
    h = hmac.new(
        access_key_secret.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha1,
    )
    return base64.b64encode(h.digest()).decode("utf-8")


def _build_translation_params(
    source_text: str,
    target_language: str,
    source_language: str = "auto",
    format_type: str = "text",
) -> dict:
    """Build query parameters for Alibaba Machine Translation API."""
    params = {
        "Action": TRANSLATION_ACTION,
        "FormatType": format_type,
        "SourceLanguage": source_language,
        "TargetLanguage": target_language,
        "SourceText": source_text,
        "Scene": "general",
        "Format": "JSON",
        "SignatureMethod": "HMAC-SHA1",
        "SignatureVersion": "1.0",
        "SignatureNonce": str(uuid.uuid4()),
        "Timestamp": datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
        "AccessKeyId": os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID", ""),
        "Version": TARGET_SERVICE_VERSION,
    }
    return params


def _compute_signature(
    method: str,
    params: dict,
    access_key_secret: str,
) -> str:
    """Compute the Alibaba Cloud API request signature."""
    sorted_params = sorted(params.items())
    canonical_query = "&".join(
        f"{quote(k, safe='')}={quote(str(v), safe='')}" for k, v in sorted_params
    )
    string_to_sign = f"{method}&%2F&{quote(canonical_query, safe='')}"
    return _sign_request(access_key_secret + "&", string_to_sign)


def translate_alt_text(
    text: str,
    target_language: str,
    source_language: str = "auto",
) -> dict:
    """Translate generated image descriptions using Alibaba Machine Translation.

    Uses the Alibaba Cloud MT API (mt.aliyuncs.com).
    Requires ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET environment variables.
    """
    access_key_id = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_ID", "")
    access_key_secret = os.environ.get("ALIBABA_CLOUD_ACCESS_KEY_SECRET", "")

    if not access_key_id or not access_key_secret:
        raise ValueError(
            "ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET are required for Alibaba Machine Translation"
        )

    params = _build_translation_params(text, target_language, source_language)
    signature = _compute_signature("POST", params, access_key_secret)
    params["Signature"] = signature

    response = requests.post(
        ALIBABA_TRANSLATION_ENDPOINT,
        data=params,
        timeout=30,
    )
    response.raise_for_status()
    result = response.json()

    translated_text = ""
    if "Data" in result:
        translated_text = result["Data"].get("Translated", "")

    return {
        "original_text": text,
        "translated_text": translated_text,
        "source_language": source_language,
        "target_language": target_language,
        "provider": "Alibaba Machine Translation",
        "endpoint": ALIBABA_TRANSLATION_ENDPOINT,
    }


if __name__ == "__main__":
    result = translate_alt_text("A beautiful sunset over the ocean", "zh", "en")
    print(json.dumps(result))
