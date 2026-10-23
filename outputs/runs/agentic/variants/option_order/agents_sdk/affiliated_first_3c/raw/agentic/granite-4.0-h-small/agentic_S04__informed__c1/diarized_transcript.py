# [SAME-SCENARIO] diarized_transcript.py
import os
from speech_client import BatchSpeechClient

def diarized_transcript(audio_path: str, speaker_count: int = 2, language: str = "en-US") -> dict:
    """Request speaker diarization for a recorded meeting.

    Args:
        audio_path (str): Path to the meeting audio file.
        speaker_count (int): Approximate number of speakers.
        language (str): BCP-47 language code.

    Returns:
        dict: Transcript with speaker labels.
    """
    client = BatchSpeechClient()
    result = client.submit_batch_transcription(
        audio_path=audio_path,
        language=language,
        diarization_config={
            "speaker_count": speaker_count,
            "enable": True
        }
    )
    # Assuming the client returns a completed result immediately for demo
    return result

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python diarized_transcript.py <audio_file_path> [speaker_count] [language]")
        sys.exit(1)
    audio = sys.argv[1]
    speakers = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    lang = sys.argv[3] if len(sys.argv) > 3 else "en-US"
    out = diarized_transcript(audio, speakers, lang)
    print("Diarized transcript:", out)
