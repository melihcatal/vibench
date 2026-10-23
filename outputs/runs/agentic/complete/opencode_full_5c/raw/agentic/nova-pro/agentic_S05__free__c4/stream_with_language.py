from speech_client import create_streaming_recognizer


def stream_with_language(language_code="en-US"):
    client, streaming_config = create_streaming_recognizer(language_code=language_code)
    # Simulate streaming recognition with language settings
    for _ in range(5):
        audio_data = b"simulated_audio_data"
        audio = types.RecognitionAudio(content=audio_data)
        request = types.StreamingRecognizeRequest(audio_content=audio.content)
        responses = client.streaming_recognize(streaming_config, [request])
        for response in responses:
            for result in response.results:
                print("Transcript: {}".format(result.alternatives[0].transcript))
