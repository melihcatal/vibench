from google.cloud import speech_v1p1beta1 as speech
import io

def transcribe_audio(audio_content: bytes, sample_rate_hertz: int, language_code: str = "en-US") -> str:
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript_parts = []
    for result in response.results:
        transcript_parts.append(result.alternatives[0].transcript)

    return " ".join(transcript_parts)
