from google.cloud import speech_v1
from google.cloud.speech_v1 import RecognitionConfig, RecognitionAudio
import io


def transcribe_synthesized_audio(audio_bytes, language_code="en-US"):
    """Transcribe synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text."""
    client = speech_v1.SpeechClient()

    audio = RecognitionAudio(content=audio_bytes)

    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,
        language_code=language_code,
        enable_automatic_punctuation=True,
        model="video",
    )

    response = client.recognize(config=config, audio=audio)

    transcripts = []
    for result in response.results:
        transcript = result.alternatives[0].transcript
        confidence = result.alternatives[0].confidence
        transcripts.append({"transcript": transcript, "confidence": confidence})

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
        }

    best_transcript = max(transcripts, key=lambda x: x["confidence"])

    original_lower = original_text.lower().strip()
    transcribed_lower = best_transcript["transcript"].lower().strip()

    is_match = original_lower == transcribed_lower

    return {
        "match": is_match,
        "confidence": best_transcript["confidence"],
        "transcribed_text": best_transcript["transcript"],
        "original_text": original_text,
        "word_error_rate": calculate_word_error_rate(
            original_text, best_transcript["transcript"]
        ),
    }


def calculate_word_error_rate(reference, hypothesis):
    """Calculate Word Error Rate between reference and hypothesis texts."""
    import re

    ref_words = re.findall(r"\w+", reference.lower())
    hyp_words = re.findall(r"\w+", hypothesis.lower())

    if not ref_words:
        return 0.0 if not hyp_words else 1.0

    from collections import Counter

    ref_counter = Counter(ref_words)
    hyp_counter = Counter(hyp_words)

    common = sum((ref_counter & hyp_counter).values())
    substitutions = sum((ref_counter - hyp_counter).values())
    insertions = sum((hyp_counter - ref_counter).values())

    total_words = len(ref_words)
    errors = substitutions + insertions

    return errors / total_words if total_words > 0 else 0.0
