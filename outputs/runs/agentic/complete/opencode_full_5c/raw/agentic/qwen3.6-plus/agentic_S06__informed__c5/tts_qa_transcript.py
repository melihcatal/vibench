import os
import time
import assemblyai as aai


def transcribe_audio_file(audio_path: str) -> str:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")

    aai.settings.api_key = api_key
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    return transcript.text


def transcribe_audio_bytes(audio_bytes: bytes) -> str:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")

    aai.settings.api_key = api_key
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_bytes)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    return transcript.text


def transcribe_with_config(
    audio_path: str,
    language_code: str = "en",
    punctuate: bool = True,
    format_text: bool = True,
) -> dict:
    api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise ValueError("ASSEMBLYAI_API_KEY environment variable is required")

    aai.settings.api_key = api_key

    config = aai.TranscriptionConfig(
        language_code=language_code,
        punctuate=punctuate,
        format_text=format_text,
    )
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_path, config=config)

    if transcript.status == aai.TranscriptStatus.error:
        raise RuntimeError(f"Transcription failed: {transcript.error}")

    return {
        "text": transcript.text,
        "words": [
            {"word": w.text, "start": w.start, "end": w.end} for w in transcript.words
        ]
        if transcript.words
        else [],
        "confidence": transcript.confidence,
        "language": transcript.language_code,
    }


def verify_synthesis(
    audio_path: str, expected_text: str, similarity_threshold: float = 0.7
) -> dict:
    result = transcribe_with_config(audio_path)
    transcribed = result["text"]

    expected_words = set(expected_text.lower().split())
    transcribed_words = set(transcribed.lower().split())

    if not expected_words:
        return {
            "passed": True,
            "transcribed": transcribed,
            "expected": expected_text,
            "word_overlap": 1.0,
        }

    overlap = len(expected_words & transcribed_words) / len(expected_words)
    passed = overlap >= similarity_threshold

    return {
        "passed": passed,
        "transcribed": transcribed,
        "expected": expected_text,
        "word_overlap": overlap,
        "confidence": result["confidence"],
    }
