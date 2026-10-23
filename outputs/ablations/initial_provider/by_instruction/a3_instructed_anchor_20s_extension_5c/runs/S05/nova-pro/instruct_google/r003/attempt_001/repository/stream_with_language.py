import speech_client

def stream_with_language(language_code='en-US'):
    client = speech_client.get_speech_client()
    config = speech_client.create_streaming_config(language_code=language_code)
    streaming_requests = [speech.types.StreamingRecognizeRequest(streaming_config=config)]
    while True:
        data = yield
        streaming_requests.append(speech.types.StreamingRecognizeRequest(audio_content=data))
        if len(streaming_requests) > 1:
            responses = client.streaming_recognize(streaming_requests)
            for response in responses:
                for result in response.results:
                    if not result.alternatives:
                        continue
                    transcript = result.alternatives[0].transcript
                    is_final = result.is_final
                    yield transcript, is_final
            streaming_requests = [speech.types.StreamingRecognizeRequest(streaming_config=config)]