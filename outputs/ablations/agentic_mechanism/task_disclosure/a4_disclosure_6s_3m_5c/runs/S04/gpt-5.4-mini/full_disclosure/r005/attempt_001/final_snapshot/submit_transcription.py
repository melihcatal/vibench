import base64
import json
import os
from typing import Any, Dict, Optional

import requests


def submit_transcription(audio_file_path: str, callback_url: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")

    headers = {"authorization": api_key}
    with open(audio_file_path, "rb") as f:
        upload_resp = requests.post(
            "https://api.assemblyai.com/v2/upload",
            headers=headers,
            data=f,
            timeout=120,
        )
    upload_resp.raise_for_status()
    upload_url = upload_resp.json()["upload_url"]

    payload: Dict[str, Any] = {
        "audio_url": upload_url,
        "speech_model": "best",
        "format_text": True,
    }
    if callback_url:
        payload["webhook_url"] = callback_url

    transcript_resp = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        headers={**headers, "content-type": "application/json"},
        data=json.dumps(payload),
        timeout=120,
    )
    transcript_resp.raise_for_status()
    return transcript_resp.json()
