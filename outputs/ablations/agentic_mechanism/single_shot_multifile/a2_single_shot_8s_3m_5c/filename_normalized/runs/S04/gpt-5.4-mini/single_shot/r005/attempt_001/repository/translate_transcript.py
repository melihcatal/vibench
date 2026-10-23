from typing import Any, Dict

from openai import OpenAI

from speech_client import get_openai_client, load_speech_settings
from speech_models import TranslateTranscriptRequest


def translate_transcript(transcript: Dict[str, Any], target_language: str) -> Dict[str, Any]:
    settings = load_speech_settings()
    client = get_openai_client(settings)
    request = TranslateTranscriptRequest(transcript=transcript, target_language=target_language)
    text = request.transcript.get("text", "") if isinstance(request.transcript, dict) else str(request.transcript)
    response = client.chat.completions.create(
        model=settings.translation_model,
        messages=[
            {"role": "system", "content": "Translate transcript text while preserving speaker labels and timestamps when present."},
            {"role": "user", "content": f"Target language: {request.target_language}\n\n{text}"},
        ],
    )
    return {"target_language": request.target_language, "translation": response.choices[0].message.content}
