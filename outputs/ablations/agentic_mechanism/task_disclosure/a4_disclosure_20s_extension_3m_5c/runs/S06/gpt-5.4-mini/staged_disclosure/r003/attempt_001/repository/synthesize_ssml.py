import os
import requests


ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"


def synthesize_ssml(ssml: str, voice_id: str, output_path: str, model_id: str = "eleven_multilingual_v2") -> None:
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is required")

    url = f"{ELEVENLABS_API_URL}/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": "audio/mpeg",
    }
    payload = {
        "text": ssml,
        "model_id": model_id,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75,
            "style": 0.0,
            "use_speaker_boost": True,
        },
    }

    response = requests.post(url, headers=headers, json=payload, timeout=120)
    response.raise_for_status()

    with open(output_path, "wb") as f:
        f.write(response.content)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 4:
        raise SystemExit("Usage: synthesize_ssml.py <ssml> <voice_id> <output_path>")

    synthesize_ssml(sys.argv[1], sys.argv[2], sys.argv[3])
