from google.cloud import speech_v1p1beta1 as speech

def get_recognition_config(
    language_code: str = "en-US",
    sample_rate_hertz: int = 16000,
    encoding: speech.RecognitionConfig.AudioEncoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
    enable_automatic_punctuation: bool = True,
    model: str = "default",
    use_enhanced: bool = False,
) -> speech.RecognitionConfig:
    """
    Creates a Google Cloud Speech-to-Text RecognitionConfig.

    Args:
        language_code: The BCP-47 language code, e.g., "en-US", "es-ES".
        sample_rate_hertz: The sample rate of the audio in Hertz.
        encoding: The audio encoding type.
        enable_automatic_punctuation: Whether to enable automatic punctuation in the transcript.
        model: The name of the model to use for recognition. "default", "command_and_search", "enhanced" etc.
        use_enhanced: Set to true to use an enhanced model for speech recognition.

    Returns:
        A speech.RecognitionConfig object.
    """
    config = speech.RecognitionConfig(
        encoding=encoding,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model=model,
        use_enhanced=use_enhanced,
    )
    return config

def get_streaming_config(config: speech.RecognitionConfig, interim_results: bool = True) -> speech.StreamingRecognitionConfig:
    """
    Creates a Google Cloud Speech-to-Text StreamingRecognitionConfig.

    Args:
        config: The RecognitionConfig to use.
        interim_results: If true, interim results (partial transcripts) are returned.

    Returns:
        A speech.StreamingRecognitionConfig object.
    """
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=interim_results,
    )
    return streaming_config


def normalize_transcript_result(response: speech.StreamingRecognizeResponse) -> dict:
    """
    Normalizes a StreamingRecognizeResponse into a simpler dictionary format.

    Args:
        response: A StreamingRecognizeResponse object.

    Returns:
        A dictionary containing 'transcript', 'is_final', and 'confidence'.
    """
    if not response.results:
        return {"transcript": "", "is_final": False, "confidence": 0.0}

    result = response.results[0]
    if not result.alternatives:
        return {"transcript": "", "is_final": False, "confidence": 0.0}

    alternative = result.alternatives[0]
    return {"transcript": alternative.transcript, "is_final": result.is_final, "confidence": alternative.confidence}

if __name__ == '__main__':
    # Example usage:
    # config = get_recognition_config(language_code="en-GB")
    # print(f"Generated config: {config}")
    #
    # streaming_config = get_streaming_config(config, interim_results=False)
    # print(f"Generated streaming config: {streaming_config}")

    # Simulate a response for normalization
    # fake_response = speech.StreamingRecognizeResponse(
    #     results=[
    #         speech.StreamingRecognitionResult(
    #             alternatives=[
    #                 speech.SpeechRecognitionAlternative(transcript="hello world", confidence=0.95)
    #             ],
    #             is_final=True,
    #             stability=1.0
    #         )
    #     ]
    # )
    # normalized = normalize_transcript_result(fake_response)
    # print(f"Normalized result: {normalized}")
    pass
