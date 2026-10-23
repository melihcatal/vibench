import assemblyai as aai

from speech_client import get_assemblyai_api_key
from speech_models import SpeechJobRequest, normalize_segments


def timestamped_transcript(audio_url: str, word_timestamps: bool = False) -> list[dict]:
    aai.settings.api_key = get_assemblyai_api_key()
    request = SpeechJobRequest(
        audio_url=audio_url,
        word_timestamps=word_timestamps,
        utterance_timestamps=not word_timestamps,
    )
    transcriber = aai.Transcriber()
    config = aai.TranscriptionConfig(
        word_boost=[], speaker_labels=False, punctuate=True
    )
    transcript = transcriber.transcribe(request.audio_url, config)
    payload = transcript.to_dict()
    return (
        payload.get("words", [])
        if request.word_timestamps
        else normalize_segments(payload)
    )
