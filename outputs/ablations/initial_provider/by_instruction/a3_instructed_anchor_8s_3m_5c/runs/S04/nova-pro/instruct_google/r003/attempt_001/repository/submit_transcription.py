from google.cloud import speech_v1p1beta1 as speech

def submit_transcription(file_path: str, project_id: str, location: str) -> str:
    client = speech.SpeechClient()
    audio = speech.RecognitionAudio(uri=file_path)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True
    )
    operation = client.long_running_recognize(config=config, audio=audio)
    print('Waiting for operation to complete...')
    return operation.name