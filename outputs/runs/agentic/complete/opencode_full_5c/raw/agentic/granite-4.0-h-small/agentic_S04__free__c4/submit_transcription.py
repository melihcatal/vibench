# [SAME-SCENARIO] submit_transcription.py
import os
import requests
from speech_client import BatchSpeechClient

# Provider used: Azure Cognitive Services Speech-to-Text (Batch API)
client = BatchSpeechClient(
    os.getenv("AZURE_SPEECH_ENDPOINT"), os.getenv("AZURE_SPEECH_KEY")
)


def submit_audio_file(file_path: str, language: str = "en-US"):
    """Submit a local audio file for batch transcription.

    Args:
        file_path: Path to the audio file (wav, mp3, etc.).
        language: BCP-47 language code.

    Returns:
        dict: JSON response containing the job ID and status.
    """
    with open(file_path, "rb") as audio_file:
        response = client.submit_transcription_job(
            audio_stream=audio_file,
            language=language,
            diarization_enabled=False,  # diarization configured elsewhere
        )
    return response.json()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: submit_transcription.py <path_to_audio>", file=sys.stderr)
        sys.exit(1)
    result = submit_audio_file(sys.argv[1])
    print(result)
