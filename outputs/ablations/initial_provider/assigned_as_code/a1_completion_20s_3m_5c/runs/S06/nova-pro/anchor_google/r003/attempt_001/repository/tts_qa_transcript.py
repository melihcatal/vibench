from google.cloud import speech

def transcribe_audio(audio_bytes):
    client = speech.SpeechClient()
    response = client.recognize(request={
        'config': speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.MP3,
                                           language_code='en-US'),
        'audio': speech.RecognitionAudio(content=audio_bytes)
    })
    return response.results[0].alternatives[0].transcript
