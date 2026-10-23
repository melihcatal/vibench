from __future__ import annotations

from google.cloud import speech

from speech_models import TranscriptResult


def transcribe_qa_sample(audio_bytes: bytes, language_code: str = "en-US", sample_rate_hertz: int = 24000) -> TranscriptResult:
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        model="latest_long",
    )
    audio = speech.RecognitionAudio(content=audio_bytes)
    response = client.recognize(config=config, audio=audio)
    transcript_parts = []
    confidence = None
    for result in response.results:
        if result.alternatives:
            transcript_parts.append(result.alternatives[0].transcript)
            confidence = result.alternatives[0].confidence
    return TranscriptResult(transcript=" ".join(transcript_parts).strip(), confidence=confidence)
