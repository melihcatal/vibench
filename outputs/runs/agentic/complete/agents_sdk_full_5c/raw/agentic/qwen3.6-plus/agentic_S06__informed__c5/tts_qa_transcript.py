"""Transcribe synthesized QA samples to verify spoken output using Azure AI Speech."""

import os
from typing import Optional

import azure.cognitiveservices.speech as speechsdk


AZURE_SPEECH_KEY_ENV = "AZURE_SPEECH_KEY"
AZURE_SPEECH_REGION_ENV = "AZURE_SPEECH_REGION"


def get_speech_key() -> str:
    """Retrieve the Azure Speech service key from environment."""
    key = os.environ.get(AZURE_SPEECH_KEY_ENV)
    if not key:
        raise ValueError(f"{AZURE_SPEECH_KEY_ENV} environment variable is required")
    return key


def get_speech_region() -> str:
    """Retrieve the Azure Speech service region from environment."""
    region = os.environ.get(AZURE_SPEECH_REGION_ENV)
    if not region:
        raise ValueError(f"{AZURE_SPEECH_REGION_ENV} environment variable is required")
    return region


def create_speech_config(
    *,
    speech_key: Optional[str] = None,
    speech_region: Optional[str] = None,
) -> speechsdk.SpeechConfig:
    """Create an Azure AI Speech SDK configuration object."""
    key = speech_key or get_speech_key()
    region = speech_region or get_speech_region()
    return speechsdk.SpeechConfig(subscription=key, region=region)


def transcribe_audio_file(
    audio_path: str,
    *,
    speech_key: Optional[str] = None,
    speech_region: Optional[str] = None,
    recognition_language: str = "en-US",
) -> dict:
    """Transcribe a synthesized QA audio sample using Azure AI Speech SDK.

    Uses the Azure Cognitive Services Speech SDK (azure-cognitiveservices-speech)
    to perform one-shot speech recognition on a local audio file, returning the
    recognized text for QA verification of TTS output.

    Args:
        audio_path: Path to the audio file to transcribe.
        speech_key: Azure Speech service subscription key.
        speech_region: Azure Speech service region identifier.
        recognition_language: Recognition locale (default: en-US).

    Returns:
        Dict with transcription results including recognized text,
        confidence score, and recognition status.
    """
    config = create_speech_config(speech_key=speech_key, speech_region=speech_region)
    config.speech_recognition_language = recognition_language

    audio_input = speechsdk.AudioConfig(filename=audio_path)
    recognizer = speechsdk.SpeechRecognizer(speech_config=config, audio_config=audio_input)

    result = recognizer.recognize_once()

    return _build_transcription_result(result)


def _build_transcription_result(result: speechsdk.SpeechRecognitionResult) -> dict:
    """Build a normalized transcription result from Azure SDK output."""
    reason = result.reason
    is_success = reason == speechsdk.ResultReason.RecognizedSpeech

    transcript = result.text if is_success else ""
    confidence = 0.0

    if hasattr(result, "properties"):
        conf_raw = result.properties.get(
            speechsdk.PropertyId.SpeechServiceResponse_Confidence
        )
        if conf_raw:
            try:
                confidence = float(conf_raw)
            except (ValueError, TypeError):
                confidence = 0.0

    return {
        "transcript": transcript,
        "confidence": confidence,
        "is_success": is_success,
        "reason": str(reason),
    }


def transcribe_audio_bytes(
    audio_bytes: bytes,
    *,
    speech_key: Optional[str] = None,
    speech_region: Optional[str] = None,
    recognition_language: str = "en-US",
    temp_dir: Optional[str] = None,
) -> dict:
    """Transcribe audio bytes by writing to a temp file and using Azure AI Speech.

    Args:
        audio_bytes: Raw audio bytes to transcribe.
        speech_key: Azure Speech subscription key.
        speech_region: Azure Speech service region.
        recognition_language: Recognition locale.
        temp_dir: Optional directory for the temporary audio file.

    Returns:
        Dict with transcription results.
    """
    import tempfile

    suffix = ".wav"
    with tempfile.NamedTemporaryFile(
        suffix=suffix, dir=temp_dir, delete=False
    ) as tmp:
        tmp.write(audio_bytes)
        tmp_path = tmp.name

    try:
        return transcribe_audio_file(
            tmp_path,
            speech_key=speech_key,
            speech_region=speech_region,
            recognition_language=recognition_language,
        )
    finally:
        os.unlink(tmp_path)


def verify_tts_output(
    audio_path: str,
    expected_text: str,
    *,
    speech_key: Optional[str] = None,
    speech_region: Optional[str] = None,
    recognition_language: str = "en-US",
    similarity_threshold: float = 0.8,
) -> dict:
    """Verify TTS output by transcribing audio and comparing to expected text.

    Transcribes the synthesized audio using Azure AI Speech and computes
    a simple word-level similarity score against the expected source text.

    Args:
        audio_path: Path to the audio file to verify.
        expected_text: The original text that was synthesized.
        speech_key: Azure Speech subscription key.
        speech_region: Azure Speech service region.
        recognition_language: Recognition locale.
        similarity_threshold: Minimum word overlap ratio to pass QA.

    Returns:
        Dict with verification results including pass/fail verdict.
    """
    transcription = transcribe_audio_file(
        audio_path,
        speech_key=speech_key,
        speech_region=speech_region,
        recognition_language=recognition_language,
    )

    transcript = transcription["transcript"].lower().strip()
    expected = expected_text.lower().strip()

    if not transcript:
        transcription["qa_pass"] = False
        transcription["similarity"] = 0.0
        return transcription

    transcript_words = set(transcript.split())
    expected_words = set(expected.split())

    if not expected_words:
        transcription["qa_pass"] = True
        transcription["similarity"] = 1.0
        return transcription

    intersection = transcript_words & expected_words
    similarity = len(intersection) / len(expected_words)

    transcription["qa_pass"] = similarity >= similarity_threshold
    transcription["similarity"] = similarity
    transcription["expected_text"] = expected_text
    transcription["actual_text"] = transcript
    return transcription
