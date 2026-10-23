# [LATER-STEP] localized_audio_preview.py
"""Generate spoken previews of translated copy using a text‑to‑speech (TTS) provider.
Provides a lightweight helper to create audio files (e.g., MP3) for each translated segment."

from __future__ import annotations
import os
import subprocess
import tempfile
from typing import Dict, Any
import json

# ---------------------------------------------------------------------------
# Provider choice – using ElevenLabs TTS API as an example
# ---------------------------------------------------------------------------
try:
    import requests
except ImportError:
    requests = None

# ---------------------------------------------------------------------------
# Configuration (environment variables)
# ---------------------------------------------------------------------------
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not ELEVENLABS_API_KEY:
    raise RuntimeError("Missing ELEVENLABS_API_KEY environment variable")

# ---------------------------------------------------------------------------
# Helper: call ElevenLabs TTS endpoint
# ---------------------------------------------------------------------------
BASE_URL = "https://api.elevenlabs.io/v1/text-to-speech/"  # placeholder endpoint


def _tts_request(text: str, voice: str = "succinct_perfect_1") -> bytes:
    """Send text to ElevenLabs and return raw audio bytes (MP3)."
    """
    headers = {
        "xi-api-key": ELEVENLABS_API_KEY,
        "Content-Type": "application/json",
    }
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "style": "standard",
        },
    }
    resp = requests.post(BASE_URL + voice, json=payload, headers=headers)
    resp.raise_for_status()
    return resp.content

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def generate_audio_for_segments(segments: List[Dict[str, Any]], output_dir: str = "./audio_previews") -> List[str]:
    """Create an MP3 file for each translated segment and return the list of paths.

    Each dict in `segments` should contain a 'translated_text' key.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    audio_paths = []
    for i, seg in enumerate(segments):
        src_id = hashlib.md5(seg.get("source_text", "").encode()).hexdigest()[:8]
        file_name = f"preview_{i}_{src_id}.mp3"
        file_path = os.path.join(output_dir, file_name)
        audio_bytes = _tts_request(seg["translated_text"], voice="succinct_perfect_1")
        with open(file_path, "wb") as f:
            f.write(audio_bytes)
        audio_paths.append(file_path)
    return audio_paths

# ---------------------------------------------------------------------------
# CLI convenience (optional)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import argparse, sys
    parser = argparse.ArgumentParser(description="Create audio previews for translated segments.")
    parser.add_argument("input_file", type=str, help="JSON file with list of segment dicts.")
    parser.add_argument("--output_dir", default="./audio_previews", help="Directory to store MP3 files.")
    args = parser.parse_args()
    with open(args.input_file) as f:
        segments = json.load(f)
    paths = generate_audio_for_segments(segments, output_dir=args.output_dir)
    print(f"Generated {len(paths)} audio preview files:")
    for p in paths:
        print(p)