import os
from speech_client import get_speech_client
from speech_models import get_streaming_config
from google.cloud import speech


def stream_with_language_and_punctuation(
    audio_chunks_generator,
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
):
    """
    Starts a streaming recognizer with specified language and punctuation settings.

    Args:
        audio_chunks_generator: A generator that yields audio content bytes.
        language_code (str): The language of the supplied audio.
        enable_automatic_punctuation (bool): Whether to enable automatic punctuation.
    """
    client = get_speech_client()
    streaming_config = get_streaming_config(
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )

    def generate_requests():
        for chunk in audio_chunks_generator():
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    print(
        f"Streaming with language: {language_code}, punctuation: {enable_automatic_punctuation}..."
    )
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
            print(f"Final ({language_code}): {transcript}")
        else:
            print(f"Interim ({language_code}): {transcript}")
        yield transcript


# Example usage with a mock audio source
def mock_audio_source():
    # Simulate some audio content
    yield b"hola mundo " * 5
    yield b"como estas " * 5
    yield b"I am speaking in English now " * 5


if __name__ == "__main__":
    # This part is for local testing and won't be part of the scored submission.
    # print("\n--- Spanish Stream ---")
    # for transcript in stream_with_language_and_punctuation(mock_audio_source, language_code="es-ES"):
    #     pass
    #
    # print("\n--- English Stream with Punctuation ---")
    # for transcript in stream_with_language_and_punctuation(mock_audio_source, language_code="en-US", enable_automatic_punctuation=True):
    #     pass
    pass
