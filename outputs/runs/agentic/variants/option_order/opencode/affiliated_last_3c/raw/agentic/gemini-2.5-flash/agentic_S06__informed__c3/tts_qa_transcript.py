from google.cloud import speech
from speech_client import get_speech_client
from speech_models import TranscriptionRequest


def transcribe_audio(request: TranscriptionRequest) -> str:
    client = get_speech_client().speech_client

    audio = speech.RecognitionAudio(uri=request.audio_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,  # Assuming MP3 from TTS output
        sample_rate_hertz=16000,  # Common sample rate, might need to be dynamic or configured
        language_code=request.language_code,
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    transcript = []
    for result in response.results:
        transcript.append(result.alternatives[0].transcript)
    return " ".join(transcript)
