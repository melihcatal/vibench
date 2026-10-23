from google.cloud import speech_v1p1beta1 as speech

RATE = 16000  # Sample rate, adjust if needed


def start_streaming_recognizer_with_settings(
    audio_generator,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
):
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model="default",
        use_enhanced=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in audio_generator
    )
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        yield transcript, result.is_final
