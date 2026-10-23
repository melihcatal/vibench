import assemblyai as aai

from speech_client import get_assemblyai_api_key
from speech_models import SpeechJobRequest, normalize_segments


def diarized_transcript(audio_url: str) -> list[dict]:
    aai.settings.api_key = get_assemblyai_api_key()
    request = SpeechJobRequest(audio_url=audio_url, diarization=True)
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(speaker_labels=request.diarization)
    transcript = transcriber.transcribe(request.audio_url, config)
    return normalize_segments(transcript.to_dict())
