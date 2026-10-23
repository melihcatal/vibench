from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client, get_recognition_config
from speech_models import build_streaming_recognize_request
import collections
import time

# A mock audio source for demonstration purposes
class MockAudioSource:
    def __init__(self, sample_rate_hertz=16000, chunk_size=3200):
        self._buff = collections.deque()
        self.sample_rate_hertz = sample_rate_hertz
        self.chunk_size = chunk_size # Corresponds to 200ms of 16-bit mono audio at 16kHz

    def start(self):
        print("Mock audio stream started. (No actual audio generated)")

    def read(self):
        # Generate some mock audio data (e.g., silence)
        # In a real scenario, this would read from a microphone or file
        time.sleep(self.chunk_size / self.sample_rate_hertz) # Simulate real-time
        return b'\x00' * self.chunk_size * 2 # 16-bit mono, so chunk_size * 2 bytes

    def stop(self):
        print("Mock audio stream stopped.")

def stream_with_language_and_punctuation(
    audio_source,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True
):
    """
    Starts a streaming recognizer with specified language and punctuation settings,
    using a provided audio source.
    """
    client = get_speech_client()
    
    # Configure recognition with language and punctuation
    config = get_recognition_config(
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    # The first request must contain the streaming config
    yield build_streaming_recognize_request(streaming_config=streaming_config)

    # Then send audio content in subsequent requests
    try:
        audio_source.start()
        while True:
            chunk = audio_source.read()
            if not chunk:
                break
            yield build_streaming_recognize_request(audio_content=chunk)
    finally:
        audio_source.stop()

def process_responses_for_language_stream(responses):
    """Processes and prints results from the streaming recognition."""
    num_chars_printed = 0
    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        
        if not result.is_final:
            overwrite_chars = ' ' * (num_chars_printed - len(transcript))
            print(f"Partial ({result.stability:.2f}): {transcript}{overwrite_chars}\r", end='')
            num_chars_printed = len(transcript)
        else:
            print(f"Final: {transcript}")
            num_chars_printed = 0
            yield transcript
