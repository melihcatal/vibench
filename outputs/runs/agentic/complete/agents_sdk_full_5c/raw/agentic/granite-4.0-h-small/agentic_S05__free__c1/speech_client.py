import os
from google.cloud import speech_v1p1beta1 as speech

# Provider: Google Cloud Speech-to-Text (hosted API: speech.googleapis.com)
# Environment variable GOOGLE_APPLICATION_CREDENTIALS points to the service account JSON.

# Helper to build a streaming recognition config with optional word_time_offsets.

def build_streaming_config(
    language_code="en-US",
    enable_autopunctuation=True,
    model: str = "default",
    enable_word_time_offsets: bool = False,
):
    """
    Returns a speech.RecognitionConfig protobuf for streaming requests.

    Args:
        language_code (str): ISO 639-1 language identifier.
        enable_autopunctuation (bool): add punctuation automatically.
        model (str): model identifier; e.g., 'default', 'video', 'command_and_search'.
        enable_word_time_offsets (bool): return start/end timestamps for each word.

    Returns:
        speech.RecognitionConfig
    """
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_autopunctuation,
        model=model,
        use_enhanced=True if model == "enhanced" else False,
        enable_word_time_offsets=enable_word_time_offsets,
    )
    return config


def create_client():
    """Instantiate a Speech-to-Text client using the default credentials."""
    # The provider hostname is inferred from the library's endpoint (speech.googleapis.com)
    return speech.SpeechClient()


def speech_to_text_stream(audio_generator):
    """
    Streams audio from an async generator to Google Cloud Speech-to-Text.

    Args:
        audio_generator: async generator yielding bytes.

    Yields:
        speech.StreamingRecognizeResponse objects.
    """
    client = create_client()
    config = build_streaming_config()
    requests = [
        speech.StreamingRecognizeRequest(streaming_config=config)
    ]
    # Send initial config request
    for req in requests:
        yield req
    # Stream audio chunks
    for audio_chunk in audio_generator:
        yield speech.StreamingRecognizeRequest(audio_content=audio_chunk)

# Example usage stub (not executed in production)
# async def audio_gen():
#     while True:
#         yield b"sample audio bytes"
# for resp in speech_to_text_stream(audio_gen()):
#     print(resp)
#     break