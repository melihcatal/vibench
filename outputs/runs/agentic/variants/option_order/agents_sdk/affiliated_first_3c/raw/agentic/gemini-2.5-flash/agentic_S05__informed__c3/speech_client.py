from google.cloud import speech

def get_speech_client():
    """Returns a Google Cloud Speech-to-Text client."""
    return speech.SpeechClient()

def get_recognition_config(
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    encoding: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
    enable_automatic_punctuation: bool = True,
    model: str = "default",
    use_enhanced: bool = False,
):
    """Returns a Google Cloud Speech-to-Text RecognitionConfig."""
    return speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model=model,
        use_enhanced=use_enhanced,
    )

def get_streaming_config(config: speech.RecognitionConfig, interim_results: bool = True):
    """Returns a Google Cloud Speech-to-Text StreamingRecognitionConfig."""
    return speech.StreamingRecognitionConfig(
        config=config,
        interim_results=interim_results,
    )
