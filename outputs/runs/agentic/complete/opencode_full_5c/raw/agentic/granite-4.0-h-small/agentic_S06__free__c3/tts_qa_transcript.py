# later-step implementation - transcribe synthesized QA samples to verify spoken output

from google.cloud import speech_v1p1beta1 as speech
from speech_models import SynthesizeResponse
from speech_client import get_azure_client

# Provider: Google Cloud Speech-to-Text (explicit import google.cloud.speech_v1p1beta1)


async def transcribe_audio(
    audio_bytes: bytes, model: str = "default", language_code: str = "en-US"
) -> str:
    """Transcribe audio bytes to text using Google Speech-to-Text."""
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        model=model,
    )
    response = await client.recognize(config=config, audio=audio)
    transcript = response.results[0].alternatives[0].transcript
    return transcript


async def verify_synthesis(request: SynthesizeRequest, audio: bytes) -> bool:
    """Synthesize then transcribe the audio to verify the spoken content matches the input text."""
    result = await transcribe_audio(audio, language_code=request.locale)
    # Simple equality check (strip whitespace/punctuation for robustness in real system)
    return result.strip().lower() == request.text.strip().lower()
