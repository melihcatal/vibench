from google.cloud import speech_v1 as speech


def transcribe_audio(audio_data):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_data)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.MP3, language_code="en-US"
    )
    response = client.recognize(config=config, audio=audio)
    return " ".join([result.alternatives[0].transcript for result in response.results])
