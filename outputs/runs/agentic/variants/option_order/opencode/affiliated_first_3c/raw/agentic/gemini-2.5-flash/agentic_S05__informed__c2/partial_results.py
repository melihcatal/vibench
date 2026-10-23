import asyncio
import sys
from google.cloud import speech

from stream_microphone import stream_microphone_audio, MicrophoneStream, RATE, CHUNK
from speech_models import StreamingRecognitionConfig


async def handle_streaming_recognition_events(
    audio_source_generator, config: StreamingRecognitionConfig
):
    client = speech.SpeechClient()
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
        # Check for transcription errors
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        is_final = result.is_final

        yield {"transcript": transcript, "is_final": is_final}


if __name__ == "__main__":

    async def microphone_audio_generator():
        with MicrophoneStream(RATE, CHUNK) as stream:
            for chunk in stream.generator():
                yield chunk

    async def main():
        config = StreamingRecognitionConfig(
            language_code="en-US", enable_automatic_punctuation=True
        )
        print("Listening for speech... (Ctrl+C to stop)")
        try:
            async for event in handle_streaming_recognition_events(
                microphone_audio_generator(), config
            ):
                if event["is_final"]:
                    sys.stdout.write(f"\rFinal: {event['transcript']}\n")
                else:
                    sys.stdout.write(
                        f"\rPartial: {event['transcript']} "
                        + " " * (80 - len(event["transcript"]) - 9)
                        + "\r"
                    )
                sys.stdout.flush()
        except KeyboardInterrupt:
            print("\nStopped.")

    asyncio.run(main())
