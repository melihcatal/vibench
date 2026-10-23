import os
import assemblyai as aai
from typing import Optional


def transcribe_audio_file(audio_file_path: str, language_code: str = "en") -> dict:
    """Transcribe synthesized QA samples to verify spoken output using AssemblyAI."""
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")

    aai.settings.api_key = api_key

    config = aai.TranscriptionConfig(
        language_code=language_code, punctuate=True, format_text=True
    )

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file_path, config=config)

    return {
        "text": transcript.text,
        "words": [
            {"text": word.text, "start": word.start, "end": word.end}
            for word in transcript.words
        ],
        "confidence": transcript.confidence,
        "audio_duration": transcript.audio_duration,
        "status": transcript.status.value,
    }


def transcribe_audio_url(audio_url: str, language_code: str = "en") -> dict:
    """Transcribe audio from URL."""
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")

    aai.settings.api_key = api_key

    config = aai.TranscriptionConfig(
        language_code=language_code, punctuate=True, format_text=True
    )

    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_url, config=config)

    return {
        "text": transcript.text,
        "words": [
            {"text": word.text, "start": word.start, "end": word.end}
            for word in transcript.words
        ],
        "confidence": transcript.confidence,
        "audio_duration": transcript.audio_duration,
        "status": transcript.status.value,
    }


def compare_transcription_with_text(transcribed_text: str, original_text: str) -> dict:
    """Compare transcribed text with original text for verification."""
    import difflib

    similarity = difflib.SequenceMatcher(
        None, transcribed_text.lower(), original_text.lower()
    ).ratio()

    return {
        "similarity_score": similarity,
        "transcribed_text": transcribed_text,
        "original_text": original_text,
        "match_percentage": similarity * 100,
    }
