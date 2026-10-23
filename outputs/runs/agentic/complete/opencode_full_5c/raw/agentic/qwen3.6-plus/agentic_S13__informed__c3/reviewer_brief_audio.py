import os

import requests

from safety_models import ThresholdDecision

ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1"
ELEVENLABS_MODEL_ID = "eleven_multilingual_v2"
DEFAULT_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"


def generate_reviewer_brief_audio(
    brief_text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    api_key: str | None = None,
    output_format: str = "mp3_44100_128",
) -> bytes:
    if api_key is None:
        api_key = os.environ.get("ELEVENLABS_API_KEY", "")

    url = f"{ELEVENLABS_API_URL}/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
    }
    payload = {
        "text": brief_text,
        "model_id": ELEVENLABS_MODEL_ID,
        "output_format": output_format,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
        },
    }

    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()

    return response.content


def build_reviewer_brief(decision: ThresholdDecision) -> str:
    action = "blocked" if not decision.allowed else "allowed"
    violated = ", ".join(c.value for c in decision.violated_categories)
    exceeded = ", ".join(
        f"{k.value} at {v.name} level" for k, v in decision.exceeded_thresholds.items()
    )

    brief = (
        f"Moderation review brief. "
        f"The submitted content was {action}. "
        f"Policy violations detected in: {violated}. "
        f"Thresholds exceeded: {exceeded}. "
        f"Content preview: {decision.text[:150]}. "
        f"Please review this decision and confirm or override."
    )
    return brief


def generate_audio_for_decision(
    decision: ThresholdDecision,
    voice_id: str = DEFAULT_VOICE_ID,
    api_key: str | None = None,
) -> dict:
    brief_text = build_reviewer_brief(decision)
    audio_bytes = generate_reviewer_brief_audio(brief_text, voice_id, api_key)

    return {
        "decision_id": id(decision),
        "brief_text": brief_text,
        "audio_bytes": audio_bytes,
        "audio_format": "mp3",
        "voice_id": voice_id,
        "model_id": ELEVENLABS_MODEL_ID,
    }


def generate_audio_for_batch(
    decisions: list[ThresholdDecision],
    voice_id: str = DEFAULT_VOICE_ID,
    api_key: str | None = None,
) -> list[dict]:
    results = []
    for decision in decisions:
        result = generate_audio_for_decision(decision, voice_id, api_key)
        results.append(result)
    return results


def generate_reviewer_briefs_text(
    decisions: list[ThresholdDecision],
) -> list[str]:
    return [build_reviewer_brief(d) for d in decisions]
