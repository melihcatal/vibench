import os
from typing import Optional, Dict, Any
from pathlib import Path


def transcribe_audio(audio_file_path: str, language_code: str = "en-US") -> str:
    """Transcribe synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text."""
    from google.cloud import speech

    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path and os.path.exists(credentials_path):
        client = speech.SpeechClient.from_service_account_json(credentials_path)
    else:
        client = speech.SpeechClient()

    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,
        language_code=language_code,
        enable_automatic_punctuation=True,
        model="latest_long",
    )

    response = client.recognize(config=config, audio=audio)

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)

    return " ".join(transcripts)


def transcribe_audio_gcs(gcs_uri: str, language_code: str = "en-US") -> str:
    """Transcribe audio from Google Cloud Storage using Google Cloud Speech-to-Text."""
    from google.cloud import speech

    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if credentials_path and os.path.exists(credentials_path):
        client = speech.SpeechClient.from_service_account_json(credentials_path)
    else:
        client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,
        language_code=language_code,
        enable_automatic_punctuation=True,
        model="latest_long",
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    response = operation.result(timeout=90)

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)

    return " ".join(transcripts)


def verify_tts_output(
    original_text: str, audio_file_path: str, language_code: str = "en-US"
) -> Dict[str, Any]:
    """Verify TTS output by comparing original text with transcribed audio."""
    transcribed_text = transcribe_audio(audio_file_path, language_code)

    original_lower = original_text.lower().strip()
    transcribed_lower = transcribed_text.lower().strip()

    words_original = set(original_lower.split())
    words_transcribed = set(transcribed_lower.split())

    common_words = words_original.intersection(words_transcribed)
    missing_words = words_original.difference(words_transcribed)

    accuracy = len(common_words) / len(words_original) if words_original else 0.0

    return {
        "original_text": original_text,
        "transcribed_text": transcribed_text,
        "accuracy": accuracy,
        "common_words": list(common_words),
        "missing_words": list(missing_words),
        "word_count_original": len(words_original),
        "word_count_transcribed": len(words_transcribed),
    }
