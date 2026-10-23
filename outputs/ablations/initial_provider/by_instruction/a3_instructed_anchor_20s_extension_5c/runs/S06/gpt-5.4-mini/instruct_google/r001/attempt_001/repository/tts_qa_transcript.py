from google.cloud import speech_v1p1beta1 as speech


def transcribe_audio(audio_content: bytes, language_code: str = "en-US") -> str:
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.MP3, language_code=language_code)
    response = client.recognize(config=config, audio=audio)
    return " ".join(result.alternatives[0].transcript for result in response.results)
