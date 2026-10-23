from google.cloud import speech


def transcribe_tts_qa_sample(audio_bytes: bytes) -> str:
    """
    Transcribes a synthesized audio sample to verify its content.
    """
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3,
        sample_rate_hertz=24000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    if response.results:
        return response.results[0].alternatives[0].transcript
    return ""
