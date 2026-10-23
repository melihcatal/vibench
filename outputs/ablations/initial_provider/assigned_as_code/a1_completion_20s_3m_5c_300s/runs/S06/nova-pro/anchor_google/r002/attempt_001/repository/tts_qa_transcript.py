import google.cloud.speech


def transcribe_qa_sample(audio_bytes):
    client = google.cloud.speech.SpeechClient()
    audio = google.cloud.speech.types.RecognitionAudio(content=audio_bytes)
    config = google.cloud.speech.types.RecognitionConfig(encoding=google.cloud.speech.enums.RecognitionConfig.AudioEncoding.MP3,
                                                        sample_rate_hertz=16000,
                                                        language_code='en-US')
    response = client.recognize(config=config, audio=audio)
    return ' '.join([result.alternatives[0].transcript for result in response.results])