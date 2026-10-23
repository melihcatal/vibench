from google.cloud import speech


def create_recognition_config(
    encoding: speech.RecognitionConfig.AudioEncoding,
    sample_rate_hertz: int,
    language_code: str,
    enable_automatic_punctuation: bool = True,
    model: str = "default",
) -> speech.RecognitionConfig:
    """
    Defines a Google Cloud Speech-to-Text RecognitionConfig.
    Uses google-cloud-speech SDK.
    """
    return speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model=model,
    )


def create_streaming_recognition_config(
    recognition_config: speech.RecognitionConfig,
    interim_results: bool = True,
) -> speech.StreamingRecognitionConfig:
    """
    Defines a Google Cloud Speech-to-Text StreamingRecognitionConfig.
    Uses google-cloud-speech SDK.
    """
    return speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=interim_results,
    )


if __name__ == "__main__":
    config = create_recognition_config(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = create_streaming_recognition_config(config)
    print(f"RecognitionConfig: {config}")
    print(f"StreamingRecognitionConfig: {streaming_config}")
