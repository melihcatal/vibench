import os
from google.cloud import speech
from google.cloud.speech import RecognitionConfig, RecognitionAudio
from speech_client import get_google_stt_client
from speech_models import TranscriptionRequest, TranscriptionResult

def transcribe_qa_sample(request: TranscriptionRequest) -> TranscriptionResult:
    client = get_google_stt_client()

    audio_encoding_map = {
        "LINEAR16": RecognitionConfig.AudioEncoding.LINEAR16,
        "MP3": RecognitionConfig.AudioEncoding.MP3,
        "OGG_OPUS": RecognitionConfig.AudioEncoding.OGG_OPUS,
        "FLAC": RecognitionConfig.AudioEncoding.FLAC,
        "MULAW": RecognitionConfig.AudioEncoding.MULAW,
        "AMR": RecognitionConfig.AudioEncoding.AMR,
        "AMR_WB": RecognitionConfig.AudioEncoding.AMR_WB,
    }
    
    config = RecognitionConfig(
        encoding=audio_encoding_map.get(request.audio_encoding, RecognitionConfig.AudioEncoding.MP3),
        sample_rate_hertz=request.sample_rate_hertz,
        language_code=request.language_code,
    )
    
    audio = RecognitionAudio(content=request.audio_content)

    try:
        response = client.recognize(config=config, audio=audio)

        transcript = ""
        confidence = 0.0

        if response.results:
            first_alternative = response.results[0].alternatives[0]
            transcript = first_alternative.transcript
            confidence = first_alternative.confidence

        return TranscriptionResult(
            transcript=transcript,
            confidence=confidence
        )

    except Exception as e:
        raise RuntimeError(f"Google Cloud Speech-to-Text API request failed: {e}")
