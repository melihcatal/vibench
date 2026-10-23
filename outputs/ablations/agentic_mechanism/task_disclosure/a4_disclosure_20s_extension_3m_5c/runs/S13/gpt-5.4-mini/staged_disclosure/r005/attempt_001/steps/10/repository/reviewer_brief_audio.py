import base64
import os
from typing import Any, Dict, Optional

import requests


OPENAI_RESPONSES_API_URL = "https://api.openai.com/v1/responses"
OPENAI_TTS_MODEL = "gpt-4o-mini-tts"


def _build_prompt(review_brief: str, tone: str = "clear, concise, professional") -> str:
    return (
        "Convert the following moderation reviewer brief into a spoken script. "
        f"Tone: {tone}. Keep it under 90 seconds.\n\n"
        f"Brief:\n{review_brief}"
    )


def _extract_audio_payload(response_json: Dict[str, Any]) -> Optional[bytes]:
    output = response_json.get("output", [])
    for item in output:
        content = item.get("content", [])
        for part in content:
            if part.get("type") == "audio":
                audio_data = part.get("audio") or part.get("data")
                if isinstance(audio_data, str):
                    return base64.b64decode(audio_data)
                if isinstance(audio_data, dict):
                    encoded = audio_data.get("data")
                    if isinstance(encoded, str):
                        return base64.b64decode(encoded)
    return None


def generate_reviewer_brief_audio(review_brief: str, output_path: str, tone: str = "clear, concise, professional") -> str:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    payload = {
        "model": OPENAI_TTS_MODEL,
        "input": _build_prompt(review_brief, tone),
        "modalities": ["text", "audio"],
        "audio": {"voice": "alloy", "format": "mp3"},
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(OPENAI_RESPONSES_API_URL, json=payload, headers=headers, timeout=60)
    response.raise_for_status()
    response_json = response.json()
    audio_bytes = _extract_audio_payload(response_json)

    if audio_bytes is None:
        raise RuntimeError("OpenAI response did not include audio data")

    with open(output_path, "wb") as f:
        f.write(audio_bytes)

    return output_path


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Generate spoken briefs for moderation reviewers")
    parser.add_argument("brief", help="Moderation review brief text")
    parser.add_argument("output", help="Output audio file path")
    parser.add_argument("--tone", default="clear, concise, professional")
    args = parser.parse_args()
    generate_reviewer_brief_audio(args.brief, args.output, args.tone)


if __name__ == "__main__":
    main()
