import asyncio
import os
from google.cloud import speech


class ChunkStreamer:
    """
    Streams audio chunks from an async source to Google Cloud Speech-to-Text.
    """

    def __init__(self, language_code="en-US", sample_rate=16000, enable_automatic_punctuation=True):
        self._language_code = language_code
        self._sample_rate = sample_rate
        self._enable_automatic_punctuation = enable_automatic_punctuation
        self._client = speech.SpeechClient()

    async def _request_generator(self, audio_data_producer):
        # The first request contains the configuration
        recognition_config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=self._sample_rate,
            language_code=self._language_code,
            enable_automatic_punctuation=self._enable_automatic_punctuation,
            # model="latest_long", # Or "latest_short", "default", etc. based on use case
            # For example, specifying a model optimized for video or phone calls:
            # model="video", # or "phone_call"
            # You can also use a custom model adaptation:
            # speech_contexts=[speech.SpeechContext(phrases=["Google", "Cloud"])],
            # For multi-channel audio, specify audio_channel_count.
            # audio_channel_count=2,
            # enable_separate_recognition_per_channel=True,
            # For specific use cases, consider enhanced models:
            # use_enhanced=True,
            # For example, for a call center:
            # model="latest_long", use_enhanced=True, ABNF for custom grammar.
            # Refer to Google Cloud Speech-to-Text documentation for a complete list of models and features.
            # The default model typically offers good performance for general speech.
            # You can also explicitly specify a specific model, e.g., 'default', 'phone_call', 'video'.
            # For instance, 'model="command_and_search"' for short commands.
        )

        streaming_config = speech.StreamingRecognitionConfig(
            config=recognition_config,
            interim_results=True,
        )
        
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)

        # Subsequent requests contain audio data
        async for chunk in audio_data_producer():
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    async def generate_transcripts(self, audio_data_producer):
        requests = self._request_generator(audio_data_producer)
        
        # The `listen_asyncloop` in google-cloud-speech SDK handles the async iteration
        # The API expects an async iterator of requests.
        # This part requires the `google-cloud-speech` library to be installed.
        # The `stream_chunks` method provides the actual streaming logic.
        # The `_request_generator` is designed to be an async generator yielding requests.
        
        responses_iterator = await self._client.streaming_recognize(requests)

        async for response in responses_iterator:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript

            if result.is_final:
                yield {"type": "final", "text": transcript, "confidence": result.alternatives[0].confidence}
            else:
                yield {"type": "interim", "text": transcript, "confidence": result.alternatives[0].confidence}


# Example of a dummy async audio producer
async def dummy_audio_producer():
    # Simulate streaming audio chunks
    for _ in range(5): # Simulate 5 chunks
        yield b'\x00' * 3200  # Example silent audio chunk (16kHz, 16-bit, 1 channel, 100ms)
        await asyncio.sleep(0.5)

async def main():
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticated via `gcloud auth application-default login`
    try:
        streamer = ChunkStreamer()
        print("Google Cloud Speech-to-Text stream started.")
        async for transcript_event in streamer.generate_transcripts(dummy_audio_producer):
            print(f"Received transcript event: {transcript_event}")

    except Exception as e:
        print(f"An error occurred in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())
