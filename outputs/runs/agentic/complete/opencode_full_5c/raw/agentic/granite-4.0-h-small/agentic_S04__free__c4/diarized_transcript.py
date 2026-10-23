# [SAME-SCENARIO] diarized_transcript.py
import os
from speech_client import BatchSpeechClient

# Provider used: Azure Cognitive Services Speech-to-Text (Batch API with diarization)
client = BatchSpeechClient(
    os.getenv("AZURE_SPEECH_ENDPOINT"), os.getenv("AZURE_SPEECH_KEY")
)


def request_diarized_transcription(
    file_path: str, language: str = "en-US", max_speakers: int = 5
):
    """Submit a batch transcription job requesting speaker diarization.

    Args:
        file_path: Path to the audio file.
        language: BCP-47 language code.
        max_speakers: Maximum number of speakers to detect.

    Returns:
        dict: Job metadata.
    """
    with open(file_path, "rb") as audio_file:
        response = client.submit_transcription_job(
            audio_stream=audio_file,
            language=language,
            diarization_enabled=True,
            diarization_max_speakers=max_speakers,
        )
    return response.json()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print(
            "Usage: diarized_transcript.py <path_to_audio> [max_speakers]",
            file=sys.stderr,
        )
        sys.exit(1)
    file_path = sys.argv[1]
    max_speakers = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    result = request_diarized_transcription(file_path, max_speakers=max_speakers)
    print(result)
