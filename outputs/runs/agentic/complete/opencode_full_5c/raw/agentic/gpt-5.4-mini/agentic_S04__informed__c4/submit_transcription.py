import os
from assemblyai import Transcriber

from speech_models import TranscriptionRequest


def submit_transcription(
    audio_path: str, speaker_labels: bool = False, word_timestamps: bool = False
):
    request = TranscriptionRequest(
        audio_url=audio_path,
        speaker_labels=speaker_labels,
        word_timestamps=word_timestamps,
    )
    transcriber = Transcriber()
    config = {
        "speaker_labels": request.speaker_labels,
        "word_timestamps": request.word_timestamps,
    }
    return transcriber.transcribe(request.audio_url, config=config)
