from typing import Any, Dict

from openai import OpenAI

from speech_client import get_openai_client, load_speech_settings
from speech_models import ArchiveSummaryRequest


def archive_summary(transcript: Dict[str, Any]) -> Dict[str, Any]:
    settings = load_speech_settings()
    client = get_openai_client(settings)
    request = ArchiveSummaryRequest(transcript=transcript)
    text = request.transcript.get("text", "") if isinstance(request.transcript, dict) else str(request.transcript)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Create a concise archive summary of the transcription results."},
            {"role": "user", "content": text},
        ],
    )
    return {"summary": completion.choices[0].message.content}
