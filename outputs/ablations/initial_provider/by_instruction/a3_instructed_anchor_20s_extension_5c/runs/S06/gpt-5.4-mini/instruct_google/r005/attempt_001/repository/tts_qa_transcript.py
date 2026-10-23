from google.cloud import speech


def transcribe_audio(audio_path: str, language_code: str = "en-US") -> str:
    client = speech.SpeechClient()
    with open(audio_path, "rb") as f:
        content = f.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(language_code=language_code, encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16)
    response = client.recognize(config=config, audio=audio)
    return " ".join(result.alternatives[0].transcript for result in response.results)
