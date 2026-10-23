from speech_client import get_speech_to_text_client
from speech_models import TranscriptionRequest, TranscriptionResponse
from google.cloud import speech_v1p1beta1 as speech


def tts_qa_transcript(request: TranscriptionRequest) -> TranscriptionResponse:
    client = get_speech_to_text_client()

    audio = speech.RecognitionAudio(content=request.audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Assuming LINEAR16 from save_audio output
        sample_rate_hertz=request.sample_rate_hertz,
        language_code=request.language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript

    return TranscriptionResponse(transcript=transcript)
