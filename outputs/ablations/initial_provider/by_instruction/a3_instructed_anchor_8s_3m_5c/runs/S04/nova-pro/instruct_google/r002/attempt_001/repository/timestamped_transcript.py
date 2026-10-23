from google.cloud import speech_v1 as speech

def timestamped_transcript(audio_file_path):
    client = speech.SpeechClient()
    with open(audio_file_path, 'rb') as audio_file:
        input_audio = audio_file.read()
    audio = speech.RecognitionAudio(content=input_audio)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_word_time_offsets=True,
    )
    operation = client.long_running_recognize(config=config, audio=audio)
    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)
    for result in response.results:
        for alternative in result.alternatives:
            for word_info in alternative.words:
                print('Word: {}, Start time: {}, End time: {}'.format(
                    word_info.word, word_info.start_time, word_info.end_time))