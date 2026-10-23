from google.cloud import speech


def transcribe_tts_audio(audio_bytes: bytes, language_code: str = "en-US") -> str:
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_bytes)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=24000,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    response = client.recognize(config=config, audio=audio)
    if response.results:
        return " ".join(
            result.alternatives[0].transcript for result in response.results
        )
    return ""
