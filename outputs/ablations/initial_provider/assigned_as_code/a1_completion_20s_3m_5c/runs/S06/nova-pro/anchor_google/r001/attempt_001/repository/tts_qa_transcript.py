from google.cloud import speech


def transcribe_tts_qa_sample(audio_bytes):
    client = speech.SpeechClient()
    response = client.recognize(config={
        "encoding": speech.RecognitionConfig.AudioEncoding.LINEAR16,
        "sample_rate_hertz": 16000,
        "language_code": "en-US"
    }, audio={
        "content": audio_bytes.decode('base64')
    })
    return response.results[0].alternatives[0].transcript