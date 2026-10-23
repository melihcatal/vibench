from typing import Any, Dict, Optional

from openai import OpenAI

from speech_client import get_openai_client, load_speech_settings
from speech_models import DiarizedTranscriptRequest, normalize_transcription_result


def diarized_transcript(audio_file_path: str, speaker_count: Optional[int] = None) -> Dict[str, Any]:
    settings = load_speech_settings()
    client = get_openai_client(settings)
    request = DiarizedTranscriptRequest(audio_file_path=audio_file_path, speaker_count=speaker_count)
    with open(request.audio_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model=settings.transcription_model,
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=["segment"],
            extra_body={"speaker_labels": True, "speaker_count": request.speaker_count},
        )
    normalized = normalize_transcription_result(transcript)
    return {"speaker_diarization": True, "transcript": normalized}
