# [SAME-SCENARIO] stream_with_language.py
import asyncio

import speech_client as sc

# Provider: Google Cloud Speech-to-Text Streaming (identified via speech_client import)

async def start_streaming_with_language(language_code="es-ES", punctuation=True, sample_rate=16000):
    """
    Helper that configures a streaming recognizer with a specific language and punctuation settings.

    Args:
        language_code: BCP-47 language identifier (default Spanish).
        punctuation: enable automatic punctuation.
        sample_rate: expected audio sample rate for the input PCM stream.
    """
    # The client library encapsulates the provider-specific configuration.
    # The underlying SDK (google-cloud-speech) is referenced inside speech_client.
    async for result in sc.recognize_streaming(language_code=language_code,
                                               enable_automatic_punctuation=punctuation):
        # Yield each recognition result (partial or final)
        yield result

# Example usage (uncomment for local testing):
# async def mic():
#     for chunk in sc.microphone_generator():
#         yield chunk
# async for r in start_streaming_with_language("fr-FR"):
#     print(r)
