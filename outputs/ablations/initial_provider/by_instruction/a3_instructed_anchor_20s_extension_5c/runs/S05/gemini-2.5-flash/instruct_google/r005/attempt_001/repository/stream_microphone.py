import pyaudio
from google.cloud import speech_v1p1beta1 as speech

RATE = 16000
CHUNK = int(RATE / 10)  # 100ms

def stream_microphone_audio():
    """Streams audio from the microphone to the Google Cloud Speech-to-Text API."""
    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        # Run in a separate thread to avoid blocking the main thread
        stream_callback=lambda in_data, frame_count, time_info, status: pyaudio.paContinue
    )

    # This is a placeholder for the actual streaming logic
    # In a real scenario, you would send `in_data` to a queue or directly to the API
    # and then yield the responses from the API.
    # For this example, we'll just yield placeholder byte chunks.
    while True:
        data = audio_stream.read(CHUNK)
        yield data

def generate_transcripts():
    """Yields interim transcripts from a streaming speech recognition."""
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    # This is a placeholder for sending actual audio to the API
    # and processing the responses.
    # In a real scenario, `requests` would come from `stream_microphone_audio`.
    # For this example, we'll just simulate responses.
    # The actual implementation would look like:
    # requests = (speech.StreamingRecognizeRequest(audio_content=chunk)
    #             for chunk in stream_microphone_audio())
    # responses = client.streaming_recognize(streaming_config, requests)

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
        MockResponse("hello", False),
        MockResponse("hello there", False),
        MockResponse("hello there how are you", True),
        MockResponse("i am doing well", False),
        MockResponse("i am doing well thank you", True),
    ]

    for response in mock_responses:
        yield response
