import os
import asyncio
from typing import Optional, List, Dict, Any
import requests

from speech_models import NormalizedTranscript


PERSPECTIVE_API_ENDPOINT = (
    "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
)


def load_perspective_config(api_key: Optional[str] = None) -> dict:
    key = api_key or os.environ.get("PERSPECTIVE_API_KEY")
    if not key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")
    return {"api_key": key}


async def check_unsafe_content(
    text: str,
    api_key: Optional[str] = None,
    attributes: Optional[List[str]] = None,
    languages: Optional[List[str]] = None,
    threshold: float = 0.7,
) -> Dict[str, Any]:
    if attributes is None:
        attributes = [
            "TOXICITY",
            "SEVERE_TOXICITY",
            "IDENTITY_ATTACK",
            "INSULT",
            "PROFANITY",
            "THREAT",
            "SEXUALLY_EXPLICIT",
        ]

    if languages is None:
        languages = ["en"]

    config = load_perspective_config(api_key)

    payload = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attributes},
        "languages": languages,
        "doNotStore": True,
    }

    params = {"key": config["api_key"]}

    loop = asyncio.get_event_loop()

    def _request():
        response = requests.post(
            PERSPECTIVE_API_ENDPOINT,
            json=payload,
            params=params,
            timeout=10,
        )
        response.raise_for_status()
        return response.json()

    result = await loop.run_in_executor(None, _request)

    flagged = {}
    for attr_name, attr_scores in result.get("attributeScores", {}).items():
        score = attr_scores.get("summaryScore", {}).get("value", 0.0)
        if score >= threshold:
            flagged[attr_name] = score

    return {
        "text": text,
        "is_unsafe": len(flagged) > 0,
        "flagged_attributes": flagged,
        "all_scores": {
            attr_name: attr_scores.get("summaryScore", {}).get("value", 0.0)
            for attr_name, attr_scores in result.get("attributeScores", {}).items()
        },
        "threshold": threshold,
    }


async def check_transcript_safety(
    transcript: NormalizedTranscript,
    api_key: Optional[str] = None,
    attributes: Optional[List[str]] = None,
    threshold: float = 0.7,
) -> Dict[str, Any]:
    result = await check_unsafe_content(
        text=transcript.text,
        api_key=api_key,
        attributes=attributes,
        threshold=threshold,
    )
    result["transcript"] = transcript
    return result


async def check_transcript_batch(
    transcripts: List[NormalizedTranscript],
    api_key: Optional[str] = None,
    attributes: Optional[List[str]] = None,
    threshold: float = 0.7,
) -> List[Dict[str, Any]]:
    tasks = [
        check_transcript_safety(
            transcript=t,
            api_key=api_key,
            attributes=attributes,
            threshold=threshold,
        )
        for t in transcripts
    ]
    return await asyncio.gather(*tasks)


async def monitor_live_captions(
    caption_stream,
    api_key: Optional[str] = None,
    attributes: Optional[List[str]] = None,
    threshold: float = 0.7,
):
    async for caption in caption_stream:
        safety_result = await check_transcript_safety(
            transcript=caption,
            api_key=api_key,
            attributes=attributes,
            threshold=threshold,
        )
        yield {
            "caption": caption,
            "safety": safety_result,
        }
