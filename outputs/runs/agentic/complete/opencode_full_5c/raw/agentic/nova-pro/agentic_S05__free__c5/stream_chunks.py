import speech_client


async def stream_chunks(audio_chunks):
    client = speech_client.get_speech_client()
    config = speech_models.create_streaming_config(
        language_code="en-US", enable_automatic_punctuation=True
    )
    streaming_recognizer = client.streaming_recognize(config)
    for chunk in audio_chunks:
        streaming_recognizer.send_audio(chunk)
        async for response in streaming_recognizer.responses:
            yield response
