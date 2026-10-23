from typing import Any, Dict

from openai import OpenAI

from speech_client import get_openai_client, load_speech_settings
from speech_models import TimestampedTranscriptRequest, normalize_transcription_result


def timestamped_transcript(audio_file_path: str, granularity: str = "word") -> Dict[str, Any]:
    settings = load_speech_settings()
    client = get_openai_client(settings)
    request = TimestampedTranscriptRequest(audio_file_path=audio_file_path, granularity=granularity)
    with open(request.audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model=settings.transcription_model,
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=[request.granularity],
        )
    normalized = normalize_transcription_result(transcript)
    return {"granularity": request.granularity, "transcript": normalized}
