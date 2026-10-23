from typing import List
from speech_client import get_speech_client
from speech_models import TranscriptSegment
import assemblyai

def get_timestamped_transcript(audio_url: str) -> List[TranscriptSegment]:
    """
    Transcribes an audio file and returns segments with word-level timestamps.

    Args:
        audio_url: The public URL of the audio file to transcribe.

    Returns:
        A list of TranscriptSegment objects representing each word.
    """
    transcriber = get_speech_client()
    transcript = transcriber.transcribe(audio_url)

    if transcript.status == assemblyai.TranscriptStatus.error:
        raise Exception(f"Transcription failed: {transcript.error}")

    if not transcript.words:
        return []

    segments = [
        TranscriptSegment(
            text=word.text,
            start=word.start,
            end=word.end
        )
        for word in transcript.words
    ]
    
    return segments
