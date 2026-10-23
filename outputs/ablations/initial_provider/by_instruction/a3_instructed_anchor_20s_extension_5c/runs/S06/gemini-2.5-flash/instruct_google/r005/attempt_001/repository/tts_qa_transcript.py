from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import RecognitionConfig, RecognitionAudio

def transcribe_audio(audio_content: bytes, language_code: str = "en-US") -> str:
    """Transcribes synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text.

    Args:
        audio_content: The audio byte stream to transcribe.
        language_code: The language of the audio (e.g., "en-US").

    Returns:
        The transcribed text.
    """
    client = speech.SpeechClient()

    audio = RecognitionAudio(content=audio_content)
    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.LINEAR16, # Assuming LINEAR16 from synthesize_text.py
        sample_rate_hertz=16000, # Common sample rate, adjust if source audio is different
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = []
    for result in response.results:
        transcript.append(result.alternatives[0].transcript)

    return " ".join(transcript)
