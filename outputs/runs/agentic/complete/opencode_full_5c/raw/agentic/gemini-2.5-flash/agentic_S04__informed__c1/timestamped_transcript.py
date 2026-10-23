from typing import List, Dict
from speech_models import TranscriptionConfig, TranscriptionResult
from submit_transcription import submit_transcription_job
from poll_transcription import poll_transcription_job


def get_timestamped_transcript(
    audio_uri: str, language_code: str = "en-US"
) -> List[Dict]:
    """Requests and returns word-level timestamps from a transcription result.

    Args:
        audio_uri: URI of the audio file to transcribe.
        language_code: The language code of the audio.

    Returns:
        A list of dictionaries, where each dictionary contains word, start_time, and end_time.
    """
    config = TranscriptionConfig(
        audio_uri=audio_uri, language_code=language_code, enable_word_time_offsets=True
    )

    print(f"Submitting transcription job for word timestamps for {audio_uri}...")
    operation_id = submit_transcription_job(config)
    print(
        f"Timestamped transcription job submitted with ID: {operation_id}. Polling for results..."
    )

    result = poll_transcription_job(operation_id)

    if result.status == "COMPLETED" and result.word_timestamps:
        return result.word_timestamps
    elif result.status == "FAILED":
        print(f"Transcription job failed: {result.transcript}")
        return []
    else:
        print("No word timestamps found or transcription still in progress.")
        return []
