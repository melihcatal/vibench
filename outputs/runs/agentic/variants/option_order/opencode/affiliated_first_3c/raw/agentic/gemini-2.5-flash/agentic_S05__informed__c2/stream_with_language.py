import asyncio
import sys
from google.cloud import speech

from stream_microphone import MicrophoneStream, RATE, CHUNK
from speech_client import get_streaming_speech_client
from speech_models import StreamingRecognitionConfig


async def stream_recognizer_with_settings(
    audio_source_generator, config: StreamingRecognitionConfig
):
    client = get_streaming_speech_client()
    streaming_config = speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=RATE,
            language_code=config.language_code,
            enable_automatic_punctuation=config.enable_automatic_punctuation,
        ),
        interim_results=True,
    )

    requests = (
        speech.StreamingRecognizeRequest(audio_content=content)
        async for content in audio_source_generator
    )

    responses = client.streaming_recognize(streaming_config, requests)

    async for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        yield result.alternatives[0].transcript


if __name__ == "__main__":

    async def microphone_audio_generator():
        with MicrophoneStream(RATE, CHUNK) as stream:
            for chunk in stream.generator():
                yield chunk

    async def main():
        # Example: Streaming with specific language (Spanish) and punctuation enabled
        config = StreamingRecognitionConfig(
            language_code="es-ES", enable_automatic_punctuation=True
        )
        print(
            f"Listening in {config.language_code} with punctuation... (Ctrl+C to stop)"
        )
        try:
            async for transcript in stream_recognizer_with_settings(
                microphone_audio_generator(), config
            ):
                sys.stdout.write(
                    "\r" + transcript + " " * (80 - len(transcript)) + "\r"
                )
                sys.stdout.flush()
        except KeyboardInterrupt:
            print("\nStopped.")

    asyncio.run(main())
