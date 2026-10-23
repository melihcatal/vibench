from google.cloud import speech_v1p1beta1 as speech

def handle_partial_results():
    client = speech.SpeechClient()
    config = speech.types.RecognitionConfig(
        encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
    )
    streaming_config = speech.types.StreamingRecognitionConfig(config=config)

    # Simulate streaming from async source
    with open('audio.raw', 'rb') as audio_file:
        audio_content = audio_file.read()

        requests = (speech.types.StreamingRecognizeRequest(audio_content=content)
                    for content in [audio_content])

        responses = client.streaming_recognize(streaming_config, requests)

        for response in responses:
            for result in response.results:
                if not result.is_final:
                    print('Interim:', result.alternatives[0].transcript)
                else:
                    print('Final:', result.alternatives[0].transcript)