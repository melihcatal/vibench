from google.cloud import speech_v1p1beta1 as speech
from speech_client import SpeechClient, TranscriptionConfig
from speech_models import TranscriptionResult, WordInfo


def timestamped_transcript(audio_file_path: str) -> TranscriptionResult:
    """
    Returns word or segment timestamps from a transcription result using Google Cloud Speech-to-Text.

    Args:
        audio_file_path: Google Cloud Storage URI (gs://) of the audio file.

    Returns:
        TranscriptionResult with word-level timestamps.
    """
    config = TranscriptionConfig(enable_word_time_offsets=True)
    client = SpeechClient(config=config)

    operation_name = client.submit_transcription(audio_file_path)

    # Poll for completion (simplified for timestamp focus)
    from poll_transcription import poll_transcription

    result = poll_transcription(operation_name)

    # Ensure word-level timestamps are present
    for segment in result.segments:
        if not segment.words:
            raise ValueError(
                "Word-level timestamps were not enabled or available in the response."
            )

    return result
