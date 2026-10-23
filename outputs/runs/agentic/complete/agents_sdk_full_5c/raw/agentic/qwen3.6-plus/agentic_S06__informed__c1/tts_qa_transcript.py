"""
[LATER-STEP] tts_qa_transcript.py
Transcribe synthesized QA samples to verify spoken output using AssemblyAI Transcripts API.
"""
from typing import Optional, Dict, Any, List
import os
import time
import requests
from speech_models import TTSResponse


ASSEMBLYAI_API_BASE = "https://api.assemblyai.com/v2"


class TranscriptError(Exception):
    """Raised when transcription fails."""
    pass


def get_assemblyai_headers(api_key: Optional[str] = None) -> Dict[str, str]:
    """Get the headers required for AssemblyAI API calls."""
    key = api_key or os.environ.get("ASSEMBLYAI_API_KEY", "")
    if not key:
        raise EnvironmentError(
            "ASSEMBLYAI_API_KEY environment variable is not set and no api_key provided."
        )
    return {
        "Authorization": key,
        "Content-Type": "application/json",
    }


def upload_audio_file(
    audio_bytes: bytes,
    api_key: Optional[str] = None,
) -> str:
    """
    Upload audio bytes to AssemblyAI and get a public URL for transcription.

    Args:
        audio_bytes: Raw audio data bytes.
        api_key: Optional AssemblyAI API key.

    Returns:
        The AssemblyAI upload URL string.
    """
    headers = get_assemblyai_headers(api_key)
    upload_url = f"{ASSEMBLYAI_API_BASE}/upload"

    try:
        response = requests.post(upload_url, headers=headers, data=audio_bytes)
        response.raise_for_status()
        result = response.json()
        return result.get("upload_url", "")
    except requests.exceptions.RequestException as e:
        raise TranscriptError(f"AssemblyAI audio upload failed: {e}") from e


def submit_transcription(
    audio_url: str,
    language_code: str = "en",
    api_key: Optional[str] = None,
) -> str:
    """
    Submit an audio URL for transcription with AssemblyAI.

    Args:
        audio_url: URL of the audio file to transcribe.
        language_code: Language code for transcription (e.g., "en", "fr", "de").
        api_key: Optional AssemblyAI API key.

    Returns:
        The transcription task ID.
    """
    headers = get_assemblyai_headers(api_key)
    transcription_url = f"{ASSEMBLYAI_API_BASE}/transcript"

    payload = {
        "audio_url": audio_url,
        "language_code": language_code,
    }

    try:
        response = requests.post(transcription_url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("id", "")
    except requests.exceptions.RequestException as e:
        raise TranscriptError(f"AssemblyAI transcription submission failed: {e}") from e


def get_transcription_result(
    transcript_id: str,
    api_key: Optional[str] = None,
    max_wait_seconds: int = 300,
    poll_interval: float = 3.0,
) -> Dict[str, Any]:
    """
    Poll for and retrieve a completed transcription result from AssemblyAI.

    Args:
        transcript_id: The transcription task ID.
        api_key: Optional AssemblyAI API key.
        max_wait_seconds: Maximum time to wait for completion.
        poll_interval: Time between poll attempts in seconds.

    Returns:
        Dictionary with transcription result including text and metadata.
    """
    headers = get_assemblyai_headers(api_key)
    result_url = f"{ASSEMBLYAI_API_BASE}/transcript/{transcript_id}"

    elapsed = 0.0
    while elapsed < max_wait_seconds:
        try:
            response = requests.get(result_url, headers=headers)
            response.raise_for_status()
            result = response.json()
            status = result.get("status", "")

            if status == "completed":
                return result
            elif status == "error":
                error_msg = result.get("error", "Unknown transcription error")
                raise TranscriptError(f"AssemblyAI transcription error: {error_msg}")

            time.sleep(poll_interval)
            elapsed += poll_interval
        except requests.exceptions.RequestException as e:
            raise TranscriptError(f"AssemblyAI polling failed: {e}") from e

    raise TranscriptError(
        f"AssemblyAI transcription timed out after {max_wait_seconds} seconds."
    )


def transcribe_tts_audio(
    audio_bytes: bytes,
    expected_text: Optional[str] = None,
    language_code: str = "en",
    api_key: Optional[str] = None,
    max_wait_seconds: int = 300,
) -> Dict[str, Any]:
    """
    Full pipeline: upload TTS audio, transcribe it, and optionally compare with expected text.

    Args:
        audio_bytes: Raw synthesized audio bytes.
        expected_text: Optional ground truth text to compare against.
        language_code: Language code for transcription.
        api_key: Optional AssemblyAI API key.
        max_wait_seconds: Maximum time to wait for transcription.

    Returns:
        Dictionary with transcription text, confidence, and optional comparison metrics.
    """
    upload_url = upload_audio_file(audio_bytes, api_key=api_key)
    transcript_id = submit_transcription(upload_url, language_code, api_key=api_key)
    result = get_transcription_result(
        transcript_id, api_key=api_key, max_wait_seconds=max_wait_seconds
    )

    transcript_text = result.get("text", "")
    confidence = result.get("confidence", 0.0)

    qa_result = {
        "transcript_text": transcript_text,
        "confidence": confidence,
        "language_code": language_code,
        "transcript_id": transcript_id,
        "provider": "assemblyai",
    }

    if expected_text:
        expected_normalized = expected_text.lower().strip()
        transcript_normalized = transcript_text.lower().strip()

        exact_match = expected_normalized == transcript_normalized
        word_error_rate = _compute_word_error_rate(
            expected_normalized, transcript_normalized
        )

        qa_result["expected_text"] = expected_text
        qa_result["exact_match"] = exact_match
        qa_result["word_error_rate"] = word_error_rate
        qa_result["qa_passed"] = exact_match or word_error_rate < 0.15

    return qa_result


def transcribe_tts_response(
    response: TTSResponse,
    expected_text: Optional[str] = None,
    language_code: str = "en",
    api_key: Optional[str] = None,
    max_wait_seconds: int = 300,
) -> Dict[str, Any]:
    """
    Transcribe audio from a TTSResponse object for QA verification.

    Args:
        response: TTSResponse containing synthesized audio bytes.
        expected_text: Optional ground truth text for comparison.
        language_code: Language code for transcription.
        api_key: Optional AssemblyAI API key.
        max_wait_seconds: Maximum time to wait for transcription.

    Returns:
        QA verification result dictionary.
    """
    return transcribe_tts_audio(
        audio_bytes=response.audio_bytes,
        expected_text=expected_text,
        language_code=language_code,
        api_key=api_key,
        max_wait_seconds=max_wait_seconds,
    )


def _compute_word_error_rate(reference: str, hypothesis: str) -> float:
    """
    Compute Word Error Rate (WER) between reference and hypothesis text.

    Args:
        reference: Expected text.
        hypothesis: Transcribed text.

    Returns:
        WER as a float (0.0 = perfect, 1.0 = all wrong).
    """
    ref_words = reference.split()
    hyp_words = hypothesis.split()

    if not ref_words:
        return 0.0 if not hyp_words else 1.0

    n_ref = len(ref_words)
    n_hyp = len(hyp_words)

    # Simple edit distance for WER calculation
    dp = [[0] * (n_hyp + 1) for _ in range(n_ref + 1)]
    for i in range(n_ref + 1):
        dp[i][0] = i
    for j in range(n_hyp + 1):
        dp[0][j] = j

    for i in range(1, n_ref + 1):
        for j in range(1, n_hyp + 1):
            if ref_words[i - 1] == hyp_words[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # deletion
                    dp[i][j - 1],      # insertion
                    dp[i - 1][j - 1],  # substitution
                )

    return dp[n_ref][n_hyp] / n_ref


if __name__ == "__main__":
    print("AssemblyAI TTS QA Transcript module loaded.")
    print("Use transcribe_tts_response() to verify synthesized speech output.")
