import os
from speech_client import get_speech_client
from speech_models import get_streaming_config
from google.cloud import speech


def process_audio_stream_for_partial_results(audio_chunks_generator):
    """
    Processes an audio stream and handles partial and final recognition events.

    Args:
        audio_chunks_generator: A generator that yields audio content bytes.
    """
    client = get_speech_client()
    streaming_config = get_streaming_config()

    def generate_requests():
        for chunk in audio_chunks_generator():
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    print("Processing audio stream for partial results...")
    requests = generate_requests()
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        if result.is_final:
            print(
                f"Final Transcript (Confidence: {result.alternatives[0].confidence:.2f}): {transcript}"
            )
        else:
            print(
                f"Partial Transcript (Stability: {result.stability:.2f}): {transcript}"
            )
        yield transcript


# Example usage with a mock audio source
def mock_audio_source():
    yield b"hello world " * 10  # Simulate some audio content
    yield b"this is a test " * 10
    yield b"of partial results " * 10
    yield b"and final transcripts " * 10


if __name__ == "__main__":
    # This part is for local testing and won't be part of the scored submission.
    # for transcript in process_audio_stream_for_partial_results(mock_audio_source):
    #     pass
    pass
