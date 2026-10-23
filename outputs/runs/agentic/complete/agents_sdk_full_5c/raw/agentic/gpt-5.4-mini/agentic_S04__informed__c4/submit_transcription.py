from typing import Any, Dict

from speech_client import configure_client, load_speech_config
from speech_models import TranscriptRequest, normalize_transcript_result


def submit_transcription(audio_path: str, language_code: str = "en") -> Dict[str, Any]:
    config = load_speech_config()
    client = configure_client()
    request = TranscriptRequest(audio_url=audio_path, language_code=language_code)

    transcript = client.transcribe(
        request.audio_url,
        language_code=request.language_code or config.language_code,
        punctuate=request.punctuate,
        format_text=request.format_text,
    )
    normalized = normalize_transcript_result(transcript)
    return {
        "transcript_id": normalized.transcript_id,
        "status": normalized.status,
        "text": normalized.text,
    }
