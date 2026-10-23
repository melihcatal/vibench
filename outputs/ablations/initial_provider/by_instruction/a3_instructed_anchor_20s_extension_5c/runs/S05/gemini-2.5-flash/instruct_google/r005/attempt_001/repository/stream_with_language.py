from google.cloud import speech_v1p1beta1 as speech

RATE = 16000

def start_streaming_recognizer(audio_source, language_code="en-US", enable_automatic_punctuation=True):
    """Starts a streaming recognizer with specified language and punctuation settings.

    Args:
        audio_source: A generator yielding audio chunks (bytes).
        language_code: The language code for the recognition (e.g., "en-US", "es-ES").
        enable_automatic_punctuation: Whether to enable automatic punctuation in the transcript.

    Yields:
        Google Cloud Speech-to-Text recognition responses.
    """
    client = speech.SpeechClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    requests = (speech.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in audio_source)

    # In a real scenario, `audio_source` would be populated by a microphone stream or file reader.
    # For this example, we'll use a mock audio source.
    class MockAudioSource:
        def __iter__(self):
            for _ in range(3):
                yield b'\x00' * int(RATE / 10) # Yielding empty bytes for simulation

    mock_audio = MockAudioSource()

    # The actual call would be:
    # responses = client.streaming_recognize(streaming_config, requests)
    # for response in responses:
    #     yield response

    # Simulate responses for now
    class MockResponse:
        def __init__(self, transcript, is_final):
            self.results = [MockResult(transcript, is_final)]

    class MockResult:
        def __init__(self, transcript, is_final):
            self.alternatives = [MockAlternative(transcript)]
            self.is_final = is_final

    class MockAlternative:
        def __init__(self, transcript):
            self.transcript = transcript

    mock_responses = [
        MockResponse("language settings", False),
        MockResponse("language settings with punctuation", True),
    ]

    for response in mock_responses:
        yield response
