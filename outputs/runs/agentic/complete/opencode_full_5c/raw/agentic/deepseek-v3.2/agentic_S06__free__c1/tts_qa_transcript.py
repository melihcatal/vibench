import os
from google.cloud import speech


def transcribe_qa_audio(audio_content, language_code="en-US"):
    """Transcribe synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text."""
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )

    response = client.recognize(config=config, audio=audio)

    transcripts = []
    for result in response.results:
        transcripts.append(
            {
                "transcript": result.alternatives[0].transcript,
                "confidence": result.alternatives[0].confidence,
                "is_final": result.is_final,
            }
        )

    return transcripts


def verify_tts_output(audio_content, expected_text, language_code="en-US"):
    """Verify TTS output matches expected text."""
    transcripts = transcribe_qa_audio(audio_content, language_code)

    if not transcripts:
        return {
            "match": False,
            "confidence": 0.0,
            "actual_transcript": "",
            "expected_text": expected_text,
            "error": "No transcription returned",
        }

    actual_transcript = transcripts[0]["transcript"]
    confidence = transcripts[0]["confidence"]

    expected_clean = expected_text.lower().strip()
    actual_clean = actual_transcript.lower().strip()

    is_match = expected_clean == actual_clean

    return {
        "match": is_match,
        "confidence": confidence,
        "actual_transcript": actual_transcript,
        "expected_text": expected_text,
        "similarity_score": calculate_similarity(expected_clean, actual_clean),
    }


def calculate_similarity(text1, text2):
    """Calculate simple text similarity."""
    words1 = set(text1.split())
    words2 = set(text2.split())

    if not words1 and not words2:
        return 1.0

    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))

    return intersection / union if union > 0 else 0.0
