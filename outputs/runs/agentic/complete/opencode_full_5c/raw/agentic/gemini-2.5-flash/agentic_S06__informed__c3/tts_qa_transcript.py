from speech_client import get_stt_client
from speech_models import TranscriptionRequest
from google.cloud import speech_v1p1beta1 as speech


def transcribe_audio(request: TranscriptionRequest) -> str:
    client = get_stt_client()

    audio = speech.RecognitionAudio(uri=request.audio_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Assuming LINEAR16 from TTS output, adjust if necessary
        sample_rate_hertz=16000,  # Assuming 16kHz from TTS output, adjust if necessary
        language_code=request.language_code,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    transcript_parts = []
    for result in response.results:
        transcript_parts.append(result.alternatives[0].transcript)

    return " ".join(transcript_parts)
