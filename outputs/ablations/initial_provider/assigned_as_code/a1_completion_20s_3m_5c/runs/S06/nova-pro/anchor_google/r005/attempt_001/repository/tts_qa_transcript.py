from google.cloud import speech


def transcribe_audio(audio_bytes):
    client = speech.SpeechClient()
    response = client.recognize(config={
        "encoding": speech.RecognitionConfig.AudioEncoding.MP3,
        "sample_rate_hertz": 16000,
        "language_code": "en-US"
    }, audio={
        "content": audio_bytes
    })
    return response.results[0].alternatives[0].transcript
