import os
import assemblyai as aai
from typing import Dict, Any


def initialize_transcriber() -> aai.Transcriber:
    """Initialize the AssemblyAI transcriber with API key from environment."""
    api_key = os.getenv("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable not set")

    aai.settings.api_key = api_key
    return aai.Transcriber()


def transcribe_audio(audio_url: str = None, audio_file: str = None) -> Dict[str, Any]:
    """Transcribe synthesized QA samples to verify spoken output using AssemblyAI."""
    transcriber = initialize_transcriber()

    config = aai.TranscriptionConfig()

    if audio_url:
        transcript = transcriber.transcribe(audio_url, config)
    elif audio_file:
        transcript = transcriber.transcribe(audio_file, config)
    else:
        raise ValueError("Either audio_url or audio_file must be provided")

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    return {
        "text": transcript.text,
        "words": [
            {"text": word.text, "start": word.start, "end": word.end}
            for word in transcript.words
        ],
        "confidence": transcript.confidence,
    }
