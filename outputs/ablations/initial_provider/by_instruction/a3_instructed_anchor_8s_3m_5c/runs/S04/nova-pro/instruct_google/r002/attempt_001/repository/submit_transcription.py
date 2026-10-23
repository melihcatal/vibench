from google.cloud import speech_v1 as speech

def submit_transcription(audio_file_path):
    client = speech.SpeechClient()
    with open(audio_file_path, 'rb') as audio_file:
        input_audio = audio_file.read()
    audio = speech.RecognitionAudio(content=input_audio)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
    )
    operation = client.long_running_recognize(config=config, audio=audio)
    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)
    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))