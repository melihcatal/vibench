import os
from google.cloud import speech_v1
from google.cloud.speech_v1 import RecognitionConfig, RecognitionAudio


def transcribe_synthesized_audio(audio_bytes, language_code="en-US"):
    """Transcribe synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text."""
    client = speech_v1.SpeechClient()

    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,
        language_code=language_code,
        enable_automatic_punctuation=True,
        model="video",
    )

    audio = RecognitionAudio(content=audio_bytes)

    response = client.recognize(config=config, audio=audio)

    transcripts = []
    for result in response.results:
        transcripts.append(
            {
                "transcript": result.alternatives[0].transcript,
                "confidence": result.alternatives[0].confidence,
            }
        )

    return transcripts


def verify_tts_accuracy(original_text, audio_bytes, language_code="en-US"):
    """Verify TTS accuracy by comparing original text with transcription."""
    transcripts = transcribe_synthesized_audio(audio_bytes, language_code)

    if not transcripts:
        return {
            "match": False,
            "confidence": 0.0,
            "transcribed_text": "",
            "original_text": original_text,
            "error": "No transcription returned",
        }

    transcribed_text = transcripts[0]["transcript"]
    confidence = transcripts[0]["confidence"]

    original_lower = original_text.lower().strip()
    transcribed_lower = transcribed_text.lower().strip()

    is_match = original_lower == transcribed_lower

    return {
        "match": is_match,
        "confidence": confidence,
        "transcribed_text": transcribed_text,
        "original_text": original_text,
        "similarity_score": calculate_text_similarity(original_text, transcribed_text),
    }


def calculate_text_similarity(text1, text2):
    """Calculate similarity between two texts."""
    from difflib import SequenceMatcher

    return SequenceMatcher(None, text1.lower(), text2.lower()).ratio()


def batch_verify_tts_samples(samples):
    """Batch verify multiple TTS samples."""
    results = []

    for sample in samples:
        original_text = sample.get("text")
        audio_bytes = sample.get("audio_bytes")
        language_code = sample.get("language_code", "en-US")

        if original_text and audio_bytes:
            result = verify_tts_accuracy(original_text, audio_bytes, language_code)
            results.append(result)

    return results


def transcribe_long_audio(gcs_uri, language_code="en-US"):
    """Transcribe long audio files from GCS."""
    client = speech_v1.SpeechClient()

    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )

    audio = RecognitionAudio(uri=gcs_uri)

    operation = client.long_running_recognize(config=config, audio=audio)

    response = operation.result(timeout=300)

    transcripts = []
    for result in response.results:
        transcripts.append(
            {
                "transcript": result.alternatives[0].transcript,
                "confidence": result.alternatives[0].confidence,
            }
        )

    return transcripts
