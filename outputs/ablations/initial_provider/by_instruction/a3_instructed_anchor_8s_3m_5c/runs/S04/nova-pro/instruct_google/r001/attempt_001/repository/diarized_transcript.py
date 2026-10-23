from google.cloud import speech_v1 as speech

def request_diarization(audio_file_path):
    client = speech.SpeechClient()
    with open(audio_file_path, 'rb') as audio_file:
        audio_content = audio_file.read()

    audio = speech.RecognitionAudio(content=audio_content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_speaker_diarization=True,
        diarization_speaker_count=2,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    for result in response.results:
        print('Speaker: {}, Transcript: {}'.format(result.speaker_tag, result.alternatives[0].transcript))