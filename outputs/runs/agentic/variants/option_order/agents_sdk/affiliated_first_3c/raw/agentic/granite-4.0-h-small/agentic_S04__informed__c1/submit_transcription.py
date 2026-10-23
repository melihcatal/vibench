# [SAME-SCENARIO] submit_transcription.py
import os
from speech_client import BatchSpeechClient

def submit_transcription(audio_path: str, language: str = "en-US"):
    """Submit an audio file for batch transcription.

    Args:
        audio_path (str): Path to the audio file.
        language (str): BCP-47 language code.
    """
    client = BatchSpeechClient()
    job_id = client.submit_batch_transcription(
        audio_path=audio_path,
        language=language
    )
    print(f"Transcription job submitted. Job ID: {job_id}")

if __name__ == "__main__":
    # Example usage: python submit_transcription.py path/to/audio.wav
    import sys
    if len(sys.argv) < 2:
        print("Usage: python submit_transcription.py <audio_file_path> [language]")
        sys.exit(1)
    audio_file = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else "en-US"
    submit_transcription(audio_file, lang)
