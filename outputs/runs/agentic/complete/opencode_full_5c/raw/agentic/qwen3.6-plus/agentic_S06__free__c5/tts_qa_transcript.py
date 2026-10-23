import os
from typing import Optional, Dict, List
from google.cloud import speech_v1p1beta1 as speech


def transcribe_qa_sample(
    audio_content: bytes,
    language_code: str = "en-US",
    sample_rate_hertz: int = 24000,
    encoding: str = "MP3",
) -> Dict[str, any]:
    client = speech.SpeechClient()

    encoding_map = {
        "MP3": speech.RecognitionConfig.AudioEncoding.MP3,
        "LINEAR16": speech.RecognitionConfig.AudioEncoding.LINEAR16,
        "OGG_OPUS": speech.RecognitionConfig.AudioEncoding.OGG_OPUS,
        "MULAW": speech.RecognitionConfig.AudioEncoding.MULAW,
        "FLAC": speech.RecognitionConfig.AudioEncoding.FLAC,
    }

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=encoding_map.get(encoding, speech.RecognitionConfig.AudioEncoding.MP3),
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_word_time_offsets=True,
        enable_automatic_punctuation=True,
    )

    response = client.recognize(config=config, audio=audio)

    transcript_text = ""
    words = []
    confidence_scores = []

    for result in response.results:
        transcript_text += result.alternatives[0].transcript
        confidence_scores.append(result.alternatives[0].confidence)
        for word_info in result.alternatives[0].words:
            words.append(
                {
                    "word": word_info.word,
                    "start_time": word_info.start_time.total_seconds(),
                    "end_time": word_info.end_time.total_seconds(),
                    "confidence": word_info.confidence,
                }
            )

    avg_confidence = (
        sum(confidence_scores) / len(confidence_scores) if confidence_scores else 0.0
    )

    return {
        "transcript": transcript_text.strip(),
        "words": words,
        "confidence": avg_confidence,
        "language_code": language_code,
        "result_count": len(response.results),
    }


def transcribe_qa_sample_from_file(
    audio_file_path: str,
    language_code: str = "en-US",
    sample_rate_hertz: int = 24000,
    encoding: str = "MP3",
) -> Dict[str, any]:
    with open(audio_file_path, "rb") as f:
        audio_content = f.read()
    return transcribe_qa_sample(
        audio_content, language_code, sample_rate_hertz, encoding
    )


def verify_transcript_against_original(
    transcript: str, original_text: str, tolerance: float = 0.8
) -> Dict[str, any]:
    transcript_normalized = transcript.lower().strip().replace(".", "").replace(",", "")
    original_normalized = (
        original_text.lower().strip().replace(".", "").replace(",", "")
    )

    transcript_words = set(transcript_normalized.split())
    original_words = set(original_normalized.split())

    if not original_words:
        return {"match": True, "accuracy": 1.0, "missing_words": [], "extra_words": []}

    matched_words = transcript_words & original_words
    accuracy = len(matched_words) / len(original_words)

    missing_words = list(original_words - transcript_words)
    extra_words = list(transcript_words - original_words)

    return {
        "match": accuracy >= tolerance,
        "accuracy": accuracy,
        "missing_words": missing_words,
        "extra_words": extra_words,
        "tolerance": tolerance,
    }


def run_qa_verification(
    audio_content: bytes,
    original_text: str,
    language_code: str = "en-US",
    sample_rate_hertz: int = 24000,
    encoding: str = "MP3",
    tolerance: float = 0.8,
) -> Dict[str, any]:
    transcription = transcribe_qa_sample(
        audio_content, language_code, sample_rate_hertz, encoding
    )

    verification = verify_transcript_against_original(
        transcription["transcript"], original_text, tolerance
    )

    return {
        "transcription": transcription,
        "verification": verification,
        "passed": verification["match"],
        "confidence": transcription["confidence"],
        "accuracy": verification["accuracy"],
    }
