import os
from google.cloud import speech_v1
from google.cloud.speech_v1 import (
    RecognitionConfig,
    RecognitionAudio,
    SpeakerDiarizationConfig,
)


def request_diarized_transcription(
    audio_file_path, language_code="en-US", min_speaker_count=2, max_speaker_count=5
):
    """Request speaker diarization for a recorded meeting using Google Cloud Speech-to-Text."""
    client = speech_v1.SpeechClient()

    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = RecognitionAudio(content=content)

    diarization_config = SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=min_speaker_count,
        max_speaker_count=max_speaker_count,
    )

    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=True,
        diarization_config=diarization_config,
        model="video",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    return operation.name


if __name__ == "__main__":
    job_id = request_diarized_transcription("meeting_audio.wav")
    print(f"Submitted diarized transcription job: {job_id}")
