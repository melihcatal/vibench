import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_TTS_MODEL = "gpt-4o-mini-tts"
OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"


@dataclass
class ReviewerBrief:
    title: str
    summary: str
    key_points: list[str]
    recommendation: str


def build_brief_text(brief: ReviewerBrief) -> str:
    points = " ".join(f"Point {i + 1}: {point}." for i, point in enumerate(brief.key_points))
    return (
        f"Reviewer brief: {brief.title}. "
        f"Summary: {brief.summary}. "
        f"{points} "
        f"Recommendation: {brief.recommendation}."
    )


def synthesize_brief_audio(
    brief: ReviewerBrief,
    output_path: str,
    voice: str = "alloy",
    response_format: str = "mp3",
) -> Dict[str, Any]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI TTS synthesis")

    payload = {
        "model": OPENAI_TTS_MODEL,
        "voice": voice,
        "input": build_brief_text(brief),
        "response_format": response_format,
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_TTS_URL, headers=headers, json=payload, timeout=120)
    response.raise_for_status()

    audio_bytes = response.content
    with open(output_path, "wb") as f:
        f.write(audio_bytes)

    return {
        "provider": "openai",
        "model": OPENAI_TTS_MODEL,
        "voice": voice,
        "output_path": output_path,
        "bytes_written": len(audio_bytes),
    }


def synthesize_brief_audio_from_json(input_json: str, output_path: str) -> Dict[str, Any]:
    data = json.loads(input_json)
    brief = ReviewerBrief(
        title=data["title"],
        summary=data["summary"],
        key_points=list(data.get("key_points", [])),
        recommendation=data["recommendation"],
    )
    return synthesize_brief_audio(brief, output_path)


def audio_b64_for_brief(brief: ReviewerBrief, voice: str = "alloy") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI TTS synthesis")

    payload = {
        "model": OPENAI_TTS_MODEL,
        "voice": voice,
        "input": build_brief_text(brief),
        "response_format": "mp3",
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_TTS_URL, headers=headers, json=payload, timeout=120)
    response.raise_for_status()
    return base64.b64encode(response.content).decode("ascii")
