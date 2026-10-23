from google.cloud import speech_v1p1beta1 as speech

def start_streaming_recognizer(language_code, enable_automatic_punctuation):
    client = speech.SpeechClient()
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation
    )
    streaming_config = speech.types.StreamingRecognitionConfig(config=config)

    print('Listening, speak now...')
    with open('audio.raw', 'rb') as audio_file:
        audio_content = audio_file.read()
        requests = (speech.types.StreamingRecognizeRequest(audio_content=content)
                    for content in [audio_content])
        responses = client.streaming_recognize(streaming_config, requests)

        for response in responses:
            for result in response.results:
                print('Transcript: {}'.format(result.alternatives[0].transcript)))

if __name__ == '__main__'):
    start_streaming_recognizer('en-US', True)