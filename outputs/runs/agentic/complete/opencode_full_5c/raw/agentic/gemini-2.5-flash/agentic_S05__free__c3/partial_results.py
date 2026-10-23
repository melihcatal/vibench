from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client, get_streaming_config
from speech_models import ResponseParser


def process_streaming_events(audio_chunks_iterable):
    """Processes streaming recognition events, handling partial and final results."""
    client = get_speech_client()
    streaming_config = get_streaming_config()
    response_parser = ResponseParser()

    def request_generator():
        yield speech.StreamingRecognizeRequest(audio_config=streaming_config)
        for chunk in audio_chunks_iterable:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(request_generator())

    for result in response_parser.parse(responses):
        if result["type"] == "interim":
            print(f"Partial: {result['transcript']}")
        elif result["type"] == "final":
            print(f"Final: {result['transcript']}")
            return result["transcript"]

    return ""


# This is a dummy iterable for demonstration purposes.
# In a real scenario, this would be an actual audio stream.
class DummyAudioChunks:
    def __init__(self, num_chunks=5):
        self.num_chunks = num_chunks
        self.current_chunk = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_chunk < self.num_chunks:
            self.current_chunk += 1
            # Return a small chunk of silence, just for demonstration
            return b"\x00" * 1600  # 100ms of silence for 16kHz, 16-bit mono
        else:
            raise StopIteration
