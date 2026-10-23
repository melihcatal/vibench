from google.cloud import speech_v1p1beta1 as speech

def start_streaming_recognizer(language_code, enable_automatic_punctuation):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config)

    print('Start speaking now...')
    with microphone_stream() as stream:
        audio_generator = stream.generator()
        requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)

        responses = client.streaming_recognize(streaming_config, requests)

        for response in responses:
            for result in response.results:
                print('Transcript: {}'.format(result.alternatives[0].transcript))

def microphone_stream():
    # This is a placeholder for actual microphone streaming implementation
    pass

if __name__ == '__main__':
    start_streaming_recognizer('en-US', True)