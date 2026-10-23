from google.cloud import speech

def start_streaming_recognizer(
    audio_source_generator,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    sample_rate_hertz: int = 16000
):
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in audio_source_generator())
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        yield transcript, result.is_final
