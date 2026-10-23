from google.cloud import speech_v1p1beta1 as speech

def transcribe_synthesized_audio(audio_bytes: bytes) -> str:
    """
    Transcribes synthesized QA samples to verify spoken output using Google Cloud Speech-to-Text.
    """
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,
        language_code="en-US",
        model="latest_long"
    )
    response = client.recognize(config=config, audio=audio)
    transcript = "".join([result.alternatives[0].transcript for result in response.results])
    return transcript