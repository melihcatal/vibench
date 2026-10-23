from __future__ import annotations

import os
import logging
from collections.abc import AsyncGenerator

import requests

from speech_models import TranscriptResult, StreamingEvent

logger = logging.getLogger(__name__)

PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"


def check_text_safety(
    text: str,
    api_key: str | None = None,
    attributes: list[str] | None = None,
    languages: list[str] | None = None,
) -> dict:
    key = api_key or os.environ.get("PERSPECTIVE_API_KEY")
    if not key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is not set")

    if attributes is None:
        attributes = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "INSULT",
            "PROFANITY",
            "THREAT",
        ]

    if languages is None:
        languages = ["en"]

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attributes},
        "languages": languages,
        "spanAnnotations": False,
    }

    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": key},
        json=payload,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def is_unsafe(
    safety_result: dict,
    threshold: float = 0.7,
) -> tuple[bool, list[str]]:
    attribute_scores = safety_result.get("attributeScores", {})
    flagged = []
    for attr_name, attr_data in attribute_scores.items():
        summary = attr_data.get("summaryScore", {})
        score = summary.get("value", 0.0)
        if score >= threshold:
            flagged.append(attr_name)
    return len(flagged) > 0, flagged


async def check_live_caption_safety(
    source: AsyncGenerator[StreamingEvent, None],
    api_key: str | None = None,
    threshold: float = 0.7,
    attributes: list[str] | None = None,
) -> AsyncGenerator[StreamingEvent, None]:
    async for event in source:
        if event.result is None or not event.result.text.strip():
            yield event
            continue

        try:
            safety_result = check_text_safety(
                text=event.result.text,
                api_key=api_key,
                attributes=attributes,
            )

            unsafe, flagged_attrs = is_unsafe(safety_result, threshold=threshold)

            if unsafe:
                logger.warning(
                    "Unsafe content detected via Perspective API: %s (flags: %s)",
                    event.result.text[:80],
                    flagged_attrs,
                )

            safety_metadata = {
                "perspective_api_unsafe": unsafe,
                "perspective_api_flags": flagged_attrs,
                "perspective_api_scores": {
                    attr: data.get("summaryScore", {}).get("value", 0.0)
                    for attr, data in safety_result.get("attributeScores", {}).items()
                },
            }

            if event.raw_payload is None:
                event.raw_payload = {}
            event.raw_payload["safety"] = safety_metadata

            yield event
        except Exception as exc:
            logger.error("Perspective API safety check error: %s", exc)
            yield event
