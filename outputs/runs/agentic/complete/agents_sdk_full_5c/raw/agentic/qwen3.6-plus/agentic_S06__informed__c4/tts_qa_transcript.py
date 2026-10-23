"""
Transcribe synthesized QA samples to verify spoken output using AssemblyAI.

Provider: AssemblyAI Transcripts API
SDK: assemblyai
Auth: ASSEMBLYAI_API_KEY
"""

import os
from typing import Optional, Dict, Any, List
import time
import tempfile
from pathlib import Path

import assemblyai

ASSEMBLYAI_API_KEY_ENV = "ASSEMBLYAI_API_KEY"


def get_assemblyai_client(api_key: Optional[str] = None) -> assemblyai.Client:
    """Create an AssemblyAI client.

    Args:
        api_key: AssemblyAI API key. Falls back to ASSEMBLYAI_API_KEY env var.

    Returns:
        Initialized assemblyai.Client instance.
    """
    key = api_key or os.environ.get(ASSEMBLYAI_API_KEY_ENV)
    if not key:
        raise ValueError(
            f"AssemblyAI API key not provided. Set {ASSEMBLYAI_API_KEY_ENV}."
        )
    return assemblyai.Client(api_key=key)


def transcribe_audio_file(
    audio_path: str,
    api_key: Optional[str] = None,
    language_code: str = "en",
    speaker_labels: bool = False,
    punctuate: bool = True,
    format_text: bool = True,
) -> Dict[str, Any]:
    """Transcribe an audio file using AssemblyAI.

    Args:
        audio_path: Path to the audio file (local or URL).
        api_key: AssemblyAI API key.
        language_code: Language code for transcription.
        speaker_labels: Whether to detect speaker changes.
        punctuate: Whether to add punctuation.
        format_text: Whether to format text (capitalize, etc.).

    Returns:
        Dict with transcription text and metadata.
    """
    client = get_assemblyai_client(api_key)

    config = assemblyai.TranscriptConfig(
        language_code=language_code,
        speaker_labels=speaker_labels,
        punctuate=punctuate,
        format_text=format_text,
    )

    # Handle local file paths
    path_obj = Path(audio_path)
    if path_obj.exists():
        transcript = client.transcripts.submit(
            audio_url=str(path_obj.resolve()),
            config=config,
        )
    else:
        # Assume it's a URL
        transcript = client.transcripts.submit(
            audio_url=audio_path,
            config=config,
        )

    # Wait for completion
    transcript.wait_for_completion()

    return {
        "text": transcript.text,
        "confidence": transcript.confidence,
        "audio_duration": transcript.audio_duration,
        "language_code": transcript.language_code,
        "status": transcript.status,
        "words": transcript.words if transcript.words else [],
        "utterances": transcript.utterances if transcript.utterances else [],
    }


def transcribe_audio_bytes(
    audio_bytes: bytes,
    api_key: Optional[str] = None,
    language_code: str = "en",
    content_type: str = "audio/mpeg",
) -> Dict[str, Any]:
    """Transcribe audio bytes using AssemblyAI.

    Writes bytes to a temporary file and uploads.

    Args:
        audio_bytes: Raw audio bytes.
        api_key: AssemblyAI API key.
        language_code: Language code for transcription.
        content_type: MIME type of the audio.

    Returns:
        Dict with transcription text and metadata.
    """
    client = get_assemblyai_client(api_key)

    # Write to temp file for upload
    suffix = ".mp3" if "mpeg" in content_type else ".wav"
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        transcript = client.transcripts.submit(
            audio_url=tmp_path,
            config=assemblyai.TranscriptConfig(
                language_code=language_code,
            ),
        )
        transcript.wait_for_completion()

        return {
            "text": transcript.text,
            "confidence": transcript.confidence,
            "audio_duration": transcript.audio_duration,
            "language_code": transcript.language_code,
            "status": transcript.status,
        }
    finally:
        Path(tmp_path).unlink(missing_ok=True)


def verify_tts_output(
    original_text: str,
    audio_path: str,
    api_key: Optional[str] = None,
    similarity_threshold: float = 0.7,
) -> Dict[str, Any]:
    """Verify TTS output by transcribing and comparing to original text.

    Uses AssemblyAI to transcribe the synthesized audio and compares
    the result to the original input text.

    Args:
        original_text: The text that was synthesized.
        audio_path: Path to the synthesized audio file.
        api_key: AssemblyAI API key.
        similarity_threshold: Minimum word overlap ratio for PASS.

    Returns:
        Dict with verification results.
    """
    transcript_result = transcribe_audio_file(
        audio_path=audio_path,
        api_key=api_key,
    )

    transcribed_text = transcript_result.get("text", "")

    # Compute simple word-level similarity
    original_words = set(original_text.lower().split())
    transcribed_words = set(transcribed_text.lower().split())

    if original_words:
        overlap = len(original_words & transcribed_words) / len(original_words)
    else:
        overlap = 0.0

    passed = overlap >= similarity_threshold

    return {
        "passed": passed,
        "original_text": original_text,
        "transcribed_text": transcribed_text,
        "word_overlap_ratio": overlap,
        "similarity_threshold": similarity_threshold,
        "confidence": transcript_result.get("confidence"),
        "audio_duration": transcript_result.get("audio_duration"),
    }


def transcribe_qa_batch(
    audio_paths: List[str],
    api_key: Optional[str] = None,
    language_code: str = "en",
) -> List[Dict[str, Any]]:
    """Batch transcribe multiple QA audio samples.

    Args:
        audio_paths: List of audio file paths.
        api_key: AssemblyAI API key.
        language_code: Language code.

    Returns:
        List of transcription results.
    """
    results = []
    for path in audio_paths:
        try:
            result = transcribe_audio_file(
                audio_path=path,
                api_key=api_key,
                language_code=language_code,
            )
            result["audio_path"] = path
            results.append(result)
        except Exception as e:
            results.append({
                "audio_path": path,
                "error": str(e),
                "status": "error",
            })
    return results
