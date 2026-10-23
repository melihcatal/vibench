from __future__ import annotations

import os

import requests


def transcribe_qa_sample(audio_bytes: bytes, filename: str = "sample.mp3") -> str:
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ASSEMBLYAI_API_KEY is required for AssemblyAI transcription"
        )
    upload_response = requests.post(
        "https://api.assemblyai.com/v2/upload",
        headers={"authorization": api_key},
        data=audio_bytes,
        timeout=60,
    )
    upload_response.raise_for_status()
    upload_url = upload_response.json()["upload_url"]
    transcript_response = requests.post(
        "https://api.assemblyai.com/v2/transcript",
        headers={"authorization": api_key, "content-type": "application/json"},
        json={
            "audio_url": upload_url,
            "language_detection": True,
            "speech_model": "best",
        },
        timeout=60,
    )
    transcript_response.raise_for_status()
    transcript_id = transcript_response.json()["id"]
    status_url = f"https://api.assemblyai.com/v2/transcript/{transcript_id}"
    for _ in range(60):
        polling = requests.get(
            status_url, headers={"authorization": api_key}, timeout=30
        )
        polling.raise_for_status()
        payload = polling.json()
        status = payload["status"]
        if status == "completed":
            return payload["text"]
        if status == "error":
            raise RuntimeError(
                payload.get("error") or "AssemblyAI transcription failed"
            )
    raise TimeoutError("AssemblyAI transcription timed out")
