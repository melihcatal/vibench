from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client, get_streaming_config
from speech_models import ResponseParser


def stream_with_language_settings(
    audio_chunks_iterable, language_code="es-ES", enable_automatic_punctuation=True
):
    """Starts a streaming recognizer with specified language and punctuation settings."""
    client = get_speech_client()
    streaming_config = get_streaming_config(
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    response_parser = ResponseParser()

    def request_generator():
        yield speech.StreamingRecognizeRequest(audio_config=streaming_config)
        for chunk in audio_chunks_iterable:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    print(
        f"Streaming with language: {language_code}, punctuation: {enable_automatic_punctuation}"
    )
    responses = client.streaming_recognize(request_generator())

    for transcript in response_parser.parse(responses):
        yield transcript


# This is a dummy iterable for demonstration purposes.
# In a real scenario, this would be an actual audio stream.
class DummyAudioChunks:
    def __init__(self, num_chunks=3):
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
