from google.cloud import speech_v1p1beta1 as speech

def streaming_recognize(language_code='en-US'):
    config = {"encoding": speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
              "sample_rate_hertz": 16000,
              "language_code": language_code,
              "max_alternatives": 1,
              "enable_automatic_punctuation": True}
    client = speech.SpeechClient()
    streaming_config = {"config": config,
                         "interim_results": True}
    requests = (speech.StreamingRecognizeRequest(audio_content=content,
                                                 streaming_config=streaming_config)
                for content in iter(lambda: client.streaming_recognize(streaming_config).result(), None))
    for response in client.streaming_recognize(requests):
        for result in response.results:
            print('Transcript: {}'.format(result.alternatives[0].transcript))

if __name__ == '__main__':
    streaming_recognize()