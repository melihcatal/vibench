# [LATER-STEP] archive_summary.py
import os
import json
from typing import List, Dict
from speech_client import BatchSpeechClient
from speech_models import TranscriptionJobResult

# Provider used: OpenAI GPT-4o mini for summarization
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
V_MODEL = "gpt-4o-mini"


def summarize_segments(segments: List[Dict[str, Any]], model: str = V_MODEL) -> str:
    """
    Concatenate all segment texts and generate a concise summary using OpenAI's model.
    Returns the summary string.
    """
    full_text = " ".join(seg["text"] for seg in segments)
    # Build the request payload for GPT-4o mini
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a concise summarizer."},
            {"role": "user", "content": full_text},
        ],
        "temperature": 0.2,
    }
    resp = httpx.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json=payload,
    )
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]


if __name__ == "__main__":
    import sys
    import httpx
    from speech_client import BatchSpeechClient

    if len(sys.argv) != 2:
        print("Usage: archive_summary.py <job_id>", file=sys.stderr)
        sys.exit(1)
    job_id = sys.argv[1]
    client = BatchSpeechClient(
        os.getenv("AZURE_SPEECH_ENDPOINT"), os.getenv("AZURE_SPEECH_KEY")
    )
    result = json.loads(
        client.get_transcription_result(job_id, include_timestamps=False)
    )
    segments = result.get("segments", [])
    summary = summarize_segments(segments)
    print(summary)
