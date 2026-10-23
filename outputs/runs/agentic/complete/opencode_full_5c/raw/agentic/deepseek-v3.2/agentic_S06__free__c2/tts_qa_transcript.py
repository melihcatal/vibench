import os
import tempfile
from google.cloud import speech_v1
from google.cloud.speech_v1 import RecognitionConfig, RecognitionAudio


def transcribe_audio(audio_content, language_code="en-US", sample_rate_hertz=24000):
    """Transcribe synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text."""
    client = speech_v1.SpeechClient()

    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=True,
        model="video",
    )

    audio = RecognitionAudio(content=audio_content)

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


def transcribe_audio_file(filepath, language_code="en-US"):
    """Transcribe audio from file."""
    client = speech_v1.SpeechClient()

    with open(filepath, "rb") as f:
        audio_content = f.read()

    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )

    audio = RecognitionAudio(content=audio_content)

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


def verify_tts_output(original_text, audio_content, language_code="en-US"):
    """Verify TTS output by comparing original text with transcription."""
    transcripts = transcribe_audio(audio_content, language_code)

    if not transcripts:
        return {
            "match": False,
            "original_text": original_text,
            "transcribed_text": "",
            "confidence": 0.0,
            "error": "No transcription returned",
        }

    transcribed_text = transcripts[0]["transcript"]
    confidence = transcripts[0]["confidence"]

    original_clean = original_text.lower().strip()
    transcribed_clean = transcribed_text.lower().strip()

    is_match = original_clean == transcribed_clean

    return {
        "match": is_match,
        "original_text": original_text,
        "transcribed_text": transcribed_text,
        "confidence": confidence,
        "similarity": calculate_text_similarity(original_clean, transcribed_clean),
    }


def calculate_text_similarity(text1, text2):
    """Calculate similarity between two texts."""
    if not text1 or not text2:
        return 0.0

    words1 = set(text1.split())
    words2 = set(text2.split())

    if not words1 or not words2:
        return 0.0

    intersection = words1.intersection(words2)
    union = words1.union(words2)

    return len(intersection) / len(union) if union else 0.0
