from speech_client import create_streaming_recognizer


def partial_results():
    client, streaming_config = create_streaming_recognizer()
    # Simulate streaming recognition events
    for _ in range(5):
        audio_data = b"simulated_audio_data"
        audio = types.RecognitionAudio(content=audio_data)
        request = types.StreamingRecognizeRequest(audio_content=audio.content)
        responses = client.streaming_recognize(streaming_config, [request])
        for response in responses:
            for result in response.results:
                if not result.is_final:
                    print(
                        "Partial transcript: {}".format(
                            result.alternatives[0].transcript
                        )
                    )
                else:
                    print(
                        "Final transcript: {}".format(result.alternatives[0].transcript)
                    )
