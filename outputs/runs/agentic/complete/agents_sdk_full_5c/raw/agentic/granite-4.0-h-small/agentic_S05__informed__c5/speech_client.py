# [HELPER] speech_client.py
import os

# Provider: Google Cloud Speech-to-Text Streaming (provider identified via GOOGLE_APPLICATION_CREDENTIALS usage)
# The module abstracts provider-specific initialization.


def build_speech_client():
    """
    Create and return a provider-specific StreamingSpeechClient.
    Currently uses Google Cloud Speech-to-Text via the SDK.
    """
    # The GOOGLE_APPLICATION_CREDENTIALS env var is expected to point to a service account JSON.
    # This is the provider-identifying signal required by the requirement.
    os.environ.setdefault('GOOGLE_APPLICATION_CREDENTIALS', './service_account.json')
    from google.cloud import speech_v1p1beta1 as speech
    client = speech.SpeechClient()
    return client

async def recognize_streaming(audio_generator, language_code="en-US", enable_automatic_punctuation=True):
    """
    Asynchronous generator delivering StreamingRecognizeResult objects from the provider.

    Args:
        audio_generator: an async iterable yielding raw PCM bytes.
        language_code: BCP-47 language identifier (default English).
        enable_automatic_punctuation: turn on punctuation.
    """
    client = build_speech_client()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)
    # Provider-specific client call / streaming call
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in audio_generator)
    async for response in client.streaming_recognize(streaming_config, requests):
        # response contains zero or more StreamingRecognitionResult objects
        for result in response.results:
            yield result

# Example minimal usage (mute for real deployment):
# async def demo(source):
#     async for result in recognize_streaming(source):
#         print(result)
