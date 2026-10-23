from speech_client import speech_client
from speech_models import TranscriptionRequest, TranscriptionResult
from poll_transcription import poll_transcription


def diarized_transcript(audio_uri: str) -> TranscriptionResult:
    request = TranscriptionRequest(
        audio_uri=audio_uri, enable_speaker_diarization=True, language_code="en-US"
    )
    operation_name = speech_client.speech_client.long_running_recognize(
        config={
            "enable_word_time_offsets": True,
            "enable_speaker_diarization": True,
            "language_code": request.language_code,
            "diarization_config": {
                "enable_speaker_diarization": True,
                "min_speaker_count": 2,
                "max_speaker_count": 4,
            },
        },
        audio={"uri": request.audio_uri},
    ).operation.name

    return poll_transcription(operation_name)
