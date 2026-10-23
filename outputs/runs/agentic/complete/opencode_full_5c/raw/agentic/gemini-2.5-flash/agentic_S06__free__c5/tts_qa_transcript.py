from google.cloud import speech_v1 as speech
import io


def transcribe_audio(
    audio_content: bytes, sample_rate_hertz: int, language_code: str = "en-US"
) -> str:
    """Transcribes synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text.

    Args:
        audio_content: The audio content as a byte string.
        sample_rate_hertz: The sample rate in Hertz of the audio.
        language_code: The language code of the audio (e.g., "en-US").

    Returns:
        The transcribed text.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,  # Assuming LINEAR16 from TTS output
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
    )

    response = client.recognize(config=config, audio=audio)

    transcript = []
    for result in response.results:
        transcript.append(result.alternatives[0].transcript)

    return " ".join(transcript)
