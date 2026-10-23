import os
from typing import Optional

import requests

from speech_models import FinalTranscript


def load_content_safety_config() -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")
    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables are required"
        )
    return {"endpoint": endpoint, "key": key}


def create_content_safety_headers(key: Optional[str] = None) -> dict:
    if key is None:
        config = load_content_safety_config()
        key = config["key"]
    return {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }


async def check_caption_safety(
    transcript: FinalTranscript,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
) -> dict:
    if endpoint is None or key is None:
        config = load_content_safety_config()
        endpoint = endpoint or config["endpoint"]
        key = key or config["key"]

    text = transcript.text
    if not text:
        return {"safe": True, "categories": {}, "text": ""}

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2024-02-15-preview"
    headers = create_content_safety_headers(key)
    payload = {
        "text": text,
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    result = response.json()

    categories = {}
    max_severity = 0
    for category_result in result.get("categoriesAnalysis", []):
        category = category_result.get("category", "")
        severity = category_result.get("severity", 0)
        categories[category] = severity
        max_severity = max(max_severity, severity)

    is_safe = max_severity <= 2

    return {
        "safe": is_safe,
        "categories": categories,
        "max_severity": max_severity,
        "text": text,
    }


async def check_captions_safety_stream(
    transcript_stream,
    endpoint: Optional[str] = None,
    key: Optional[str] = None,
    unsafe_callback=None,
):
    if endpoint is None or key is None:
        config = load_content_safety_config()
        endpoint = endpoint or config["endpoint"]
        key = key or config["key"]

    async for transcript in transcript_stream:
        if isinstance(transcript, FinalTranscript) and transcript.text:
            safety_result = await check_caption_safety(
                transcript, endpoint=endpoint, key=key
            )
            if not safety_result["safe"] and unsafe_callback:
                await unsafe_callback(safety_result)
            yield safety_result
        elif hasattr(transcript, "final") and transcript.final:
            safety_result = await check_caption_safety(
                transcript.final, endpoint=endpoint, key=key
            )
            if not safety_result["safe"] and unsafe_callback:
                await unsafe_callback(safety_result)
            yield safety_result
