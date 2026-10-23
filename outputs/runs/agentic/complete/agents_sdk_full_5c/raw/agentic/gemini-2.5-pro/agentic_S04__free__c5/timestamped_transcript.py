from typing import List, Dict, Union
from speech_client import get_transcriber

def get_timestamped_transcript(audio_url: str) -> List[Dict[str, Union[str, int]]]:
    """
    Transcribes an audio file and returns a list of words with their timestamps.

    Args:
        audio_url: The public URL of the audio file.

    Returns:
        A list of word objects, each containing the text, start, and end time.
    """
    transcriber = get_transcriber()
    transcript = transcriber.transcribe(audio_url)

    if transcript.error:
        raise Exception(f"Timestamped transcription failed: {transcript.error}")

    if not transcript.words:
        return []

    return [
        {"text": word.text, "start": word.start, "end": word.end}
        for word in transcript.words
    ]
