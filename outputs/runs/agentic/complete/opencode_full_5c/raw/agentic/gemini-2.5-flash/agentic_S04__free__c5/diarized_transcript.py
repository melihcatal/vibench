import os
import sys
from speech_client import SpeechClient
from speech_models import TranscriptionRequest, TranscriptionConfig, TranscriptionAudio


def submit_diarized_transcription_job(
    gcs_uri: str,
    language_code: str = "en-US",
    speaker_count: int = 2,
) -> str:
    """
    Submits an audio file for batch transcription with speaker diarization enabled.

    Args:
        gcs_uri: The Google Cloud Storage URI of the audio file (e.g., "gs://bucket/audio.flac").
        language_code: The language code for the audio (e.g., "en-US").
        speaker_count: The number of speakers expected in the audio.

    Returns:
        The name of the long-running operation.
    """
    client = SpeechClient()
    audio = TranscriptionAudio(uri=gcs_uri)
    config = TranscriptionConfig(
        language_code=language_code,
        enable_speaker_diarization=True,
        diarization_speaker_count=speaker_count,
        enable_word_time_offsets=True,  # Recommended for diarization to see speaker tags per word
    )

    # The actual submission happens here with diarization config
    operation = client.submit_long_running_recognize(audio, config)
    print(
        f"Submitted diarized transcription job for {gcs_uri}. Operation name: {operation.operation_id}"
    )
    return operation.operation_id


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "Usage: python diarized_transcript.py <gcs_uri> [language_code] [speaker_count]"
        )
        sys.exit(1)

    gcs_uri = sys.argv[1]
    language_code = sys.argv[2] if len(sys.argv) > 2 else "en-US"
    speaker_count = int(sys.argv[3]) if len(sys.argv) > 3 else 2

    # For demonstration, ensure GOOGLE_APPLICATION_CREDENTIALS is set in your environment
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    operation_name = submit_diarized_transcription_job(
        gcs_uri, language_code, speaker_count
    )
    print(f"Operation ID for diarized transcript: {operation_name}")
    print(
        "You can use poll_transcription.py with this operation ID to retrieve results."
    )
