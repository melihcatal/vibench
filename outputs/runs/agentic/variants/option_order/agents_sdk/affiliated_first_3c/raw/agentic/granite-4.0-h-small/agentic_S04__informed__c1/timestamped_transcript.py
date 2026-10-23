# [SAME-SCENARIO] timestamped_transcript.py
import os
from speech_client import BatchSpeechClient

def timestamped_transcript(audio_path: str, language: str = "en-US") -> dict:
    """Return word or segment timestamps from a transcription result.

    Args:
        audio_path (str): Path to the audio file.
        language (str): BCP-47 language code.

    Returns:
        dict: Timestamped transcript.
    """
    client = BatchSpeechClient()
    result = client.submit_batch_transcription(
        audio_path=audio_path,
        language=language,
        timestamping=True
    )
    return result

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python timestamped_transcript.py <audio_file_path> [language] [timestamp_format=json|srt]")
        sys.exit(1)
    audio = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else "en-US"
    fmt = sys.argv[3] if len(sys.argv) > 3 else "json"
    out = timestamped_transcript(audio, lang)
    if fmt == "srt":
        # Very simple conversion (demo)
        print("Converting to SRT is not implemented in this demo.")
    else:
        print("Timestamped transcript (JSON):", out)
