"""Transcribe synthesized QA samples to verify spoken output using AssemblyAI Transcripts API."""

import os
import time
from typing import Optional, Dict, Any
import assemblyai
from assemblyai import Transcriber, TranscriptConfig

from speech_models import TTSResponse


def transcribe_qa_sample(
    audio_file_path: str,
    api_key: Optional[str] = None,
    language_code: str = "en",
) -> Dict[str, Any]:
    """Transcribe a synthesized QA audio sample using AssemblyAI to verify spoken output.

    Args:
        audio_file_path: Path to the audio file to transcribe.
        api_key: AssemblyAI API key (defaults to ASSEMBLYAI_API_KEY env var).
        language_code: Language code for transcription (e.g., 'en', 'de', 'ja').

    Returns:
        Dict with 'text', 'confidence', 'words', and 'status'.

    Raises:
        EnvironmentError: If ASSEMBLYAI_API_KEY is not set.
        RuntimeError: If transcription fails.
    """
    if api_key is None:
        api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ASSEMBLYAI_API_KEY environment variable is required. "
            "Set it to your AssemblyAI API key from https://www.assemblyai.com/"
        )

    assemblyai.settings.api_key = api_key

    transcriber = Transcriber()

    config = TranscriptConfig(
        language_code=language_code,
        speaker_labels=False,
        punctuate=True,
        format_text=True,
    )

    transcript = transcriber.transcribe(audio_file_path, config=config)
    transcript.wait_for_completion()

    if transcript.status == "error":
        raise RuntimeError(
            f"AssemblyAI transcription failed: {transcript.error}"
        )

    return {
        "text": transcript.text,
        "confidence": transcript.confidence,
        "words": [
            {
                "word": w.text,
                "confidence": w.confidence,
                "start": round(w.start, 2),
                "end": round(w.end, 2),
            }
            for w in transcript.words
        ],
        "status": transcript.status,
        "audio_duration": transcript.audio_duration,
        "language_code": transcript.language_code,
    }


def transcribe_qa_bytes(
    audio_bytes: bytes,
    api_key: Optional[str] = None,
    language_code: str = "en",
) -> Dict[str, Any]:
    """Transcribe audio bytes from a TTSResponse using AssemblyAI.

    This writes the bytes to a temporary file, transcribes it, then cleans up.

    Args:
        audio_bytes: Raw audio bytes from TTSResponse.
        api_key: AssemblyAI API key.
        language_code: Language code for transcription.

    Returns:
        Dict with transcription results.
    """
    import tempfile

    if api_key is None:
        api_key = os.environ.get("ASSEMBLYAI_API_KEY")
    if not api_key:
        raise EnvironmentError("ASSEMBLYAI_API_KEY environment variable is required.")

    assemblyai.settings.api_key = api_key

    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        result = transcribe_qa_sample(tmp_path, api_key=api_key, language_code=language_code)
        return result
    finally:
        os.unlink(tmp_path)


def verify_tts_output(
    tts_response: TTSResponse,
    original_text: str,
    api_key: Optional[str] = None,
    language_code: str = "en",
    word_accuracy_threshold: float = 0.8,
) -> Dict[str, Any]:
    """Verify TTS output quality by transcribing and comparing to original text.

    Args:
        tts_response: TTSResponse with audio_bytes to verify.
        original_text: The original text that was synthesized.
        api_key: AssemblyAI API key.
        language_code: Language code for transcription.
        word_accuracy_threshold: Minimum word accuracy ratio to pass QA.

    Returns:
        Dict with 'passed' (bool), 'transcribed_text', 'original_text',
        'word_accuracy', 'confidence', and 'details'.
    """
    transcription = transcribe_qa_bytes(
        tts_response.audio_bytes,
        api_key=api_key,
        language_code=language_code,
    )

    transcribed = transcription["text"].strip().lower()
    original = original_text.strip().lower()

    original_words = set(original.split())
    transcribed_words = set(transcribed.split())

    if original_words:
        matched = original_words & transcribed_words
        word_accuracy = len(matched) / len(original_words)
    else:
        word_accuracy = 1.0 if not transcribed_words else 0.0

    passed = word_accuracy >= word_accuracy_threshold

    return {
        "passed": passed,
        "transcribed_text": transcription["text"],
        "original_text": original_text,
        "word_accuracy": round(word_accuracy, 4),
        "confidence": transcription["confidence"],
        "details": {
            "original_words": len(original_words),
            "transcribed_words": len(transcribed_words),
            "matched_words": len(original_words & transcribed_words),
            "audio_duration": transcription.get("audio_duration"),
        },
    }


if __name__ == "__main__":
    # Example: transcribe a local audio file for QA verification
    print("AssemblyAI QA Transcription verifier ready.")
    print("Set ASSEMBLYAI_API_KEY and call verify_tts_output() with a TTSResponse.")
