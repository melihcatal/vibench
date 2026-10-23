import requests

from speech_client import load_azure_content_safety_config
from speech_models import (
    ModerationResult,
    ModerationCategory,
    normalize_azure_safety_response,
)


def moderate_transcript_text(text: str, categories: list = None) -> ModerationResult:
    config = load_azure_content_safety_config()

    if categories is None:
        categories = config.default_categories

    endpoint = config.endpoint.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze"

    params = {
        "api-version": config.api_version,
    }

    headers = {
        "Ocp-Apim-Subscription-Key": config.api_key,
        "Content-Type": "application/json",
    }

    body = {
        "text": text,
        "categories": categories,
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(
        url,
        params=params,
        headers=headers,
        json=body,
    )
    response.raise_for_status()

    raw_response = response.json()
    return normalize_azure_safety_response(raw_response, text)


def moderate_transcript_segments(segments: list, categories: list = None) -> list:
    results = []
    for seg in segments:
        if isinstance(seg, dict):
            text = seg.get("text", seg.get("original_text", ""))
            speaker = seg.get("speaker")
        else:
            text = seg.text if hasattr(seg, "text") else str(seg)
            speaker = getattr(seg, "speaker", None)

        moderation_result = moderate_transcript_text(text, categories)
        results.append(
            {
                "text": text,
                "speaker": speaker,
                "moderation": moderation_result,
            }
        )

    return results


def batch_moderate_transcript(texts: list, categories: list = None) -> list:
    config = load_azure_content_safety_config()

    if categories is None:
        categories = config.default_categories

    endpoint = config.endpoint.rstrip("/")
    url = f"{endpoint}/contentsafety/text:analyze"

    params = {
        "api-version": config.api_version,
    }

    headers = {
        "Ocp-Apim-Subscription-Key": config.api_key,
        "Content-Type": "application/json",
    }

    body = {
        "text": "\n\n---SEGMENT---\n\n".join(texts),
        "categories": categories,
        "outputType": "EightSeverityLevels",
    }

    response = requests.post(
        url,
        params=params,
        headers=headers,
        json=body,
    )
    response.raise_for_status()

    raw_response = response.json()
    return normalize_azure_safety_response(raw_response, body["text"])
