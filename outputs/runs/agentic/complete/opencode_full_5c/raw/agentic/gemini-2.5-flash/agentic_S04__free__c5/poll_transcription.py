import os
import sys
import time
from speech_client import SpeechClient
from speech_models import TranscriptionResponse


def poll_transcription_job(
    operation_name: str, timeout: int = 3600
) -> TranscriptionResponse:
    """
    Polls a Google Cloud Speech-to-Text long-running transcription operation until completion.

    Args:
        operation_name: The name of the long-running operation to poll.
        timeout: The maximum number of seconds to wait for the operation to complete.

    Returns:
        A TranscriptionResponse object containing the transcription results.
    """
    client = SpeechClient()
    print(f"Polling operation: {operation_name}. This may take some time...")

    # The actual polling happens here
    transcription_response = client.poll_operation_until_done(
        operation_name, timeout=timeout
    )
    print(f"Transcription operation {operation_name} completed.")
    return transcription_response


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python poll_transcription.py <operation_name>")
        sys.exit(1)

    operation_name = sys.argv[1]

    # For demonstration, ensure GOOGLE_APPLICATION_CREDENTIALS is set in your environment
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    try:
        response = poll_transcription_job(operation_name)
        print("\n--- Transcription Results ---")
        for i, result in enumerate(response.results):
            print(f"Segment {i + 1}:")
            for alt in result.alternatives:
                print(f"  Transcript: {alt.transcript}")
                if alt.confidence:
                    print(f"  Confidence: {alt.confidence:.2f}")
                if alt.words:
                    print("  Words (first 5):")
                    for word_info in alt.words[:5]:
                        speaker_info = (
                            f" (Speaker {word_info.speaker_tag})"
                            if word_info.speaker_tag is not None
                            else ""
                        )
                        print(
                            f"    {word_info.word} [{word_info.start_time:.2f}s-{word_info.end_time:.2f}s]{speaker_info}"
                        )
            print()

    except Exception as e:
        print(f"Error polling transcription job: {e}")
        sys.exit(1)
