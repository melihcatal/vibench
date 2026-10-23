from google.cloud import speech

def transcribe_audio(audio_content):
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(encoding=speech.RecognitionConfig.AudioEncoding.MP3, language_code='en-US')
    response = client.recognize(config=config, audio=audio)
    return response.results[0].alternatives[0].transcript