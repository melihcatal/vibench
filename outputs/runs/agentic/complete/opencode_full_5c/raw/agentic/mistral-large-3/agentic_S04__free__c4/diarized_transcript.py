from google.cloud import speech_v1p1beta1 as speech
from speech_client import SpeechClient, TranscriptionConfig
from speech_models import TranscriptionResult


def diarized_transcript(
    audio_file_path: str, speaker_count: int
) -> TranscriptionResult:
    """
    Requests speaker diarization for a recorded meeting using Google Cloud Speech-to-Text.

    Args:
        audio_file_path: Google Cloud Storage URI (gs://) of the audio file.
        speaker_count: Number of speakers to diarize.

    Returns:
        TranscriptionResult with speaker-tagged segments.
    """
    config = TranscriptionConfig(diarization_speaker_count=speaker_count)
    client = SpeechClient(config=config)

    operation_name = client.submit_transcription(audio_file_path)

    # Poll for completion (simplified for diarization focus)
    from poll_transcription import poll_transcription

    return poll_transcription(operation_name)
