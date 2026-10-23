from speech_client import get_speech_to_text_client
from speech_models import TranscriptionRequest, TranscriptionResponse
from google.cloud import speech


def tts_qa_transcript(request: TranscriptionRequest) -> TranscriptionResponse:
    client = get_speech_to_text_client()

    audio = speech.RecognitionAudio(content=request.audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=request.language_code,
    )

    response = client.recognize(config=config, audio=audio)

    if not response.results:
        return TranscriptionResponse(transcript="", confidence=0.0)

    result = response.results[0]
    best_alternative = result.alternatives[0]

    return TranscriptionResponse(
        transcript=best_alternative.transcript,
        confidence=best_alternative.confidence,
    )
