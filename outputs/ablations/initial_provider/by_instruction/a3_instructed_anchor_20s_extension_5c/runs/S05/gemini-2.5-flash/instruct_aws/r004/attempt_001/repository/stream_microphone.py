import asyncio
import boto3
from botocore.exceptions import ClientError
from typing import AsyncGenerator

# Placeholder for actual microphone streaming
async def get_audio_stream() -> AsyncGenerator[bytes, None]:
    """
    Simulates an asynchronous audio stream from a microphone.
    In a real application, this would read from an audio input device.
    """
    # Simulate streaming audio chunks
    for i in range(5):
        yield b"simulated audio chunk " + str(i).encode()
        await asyncio.sleep(0.1)

async def stream_microphone_audio_aws(
    language_code: str = "en-US",
    sample_rate: int = 16000
) -> AsyncGenerator[str, None]:
    """
    Streams microphone audio to AWS Transcribe and yields interim transcripts.
    """
    client = boto3.client("transcribe", region_name="us-east-1") # AWS region_name is a provider-identifying signal

    async def mic_stream():
        async for chunk in get_audio_stream():
            yield {
                "AudioEvent": {
                    "AudioChunk": chunk
                }
            }

    try:
        response = await client.start_stream_transcription(
            LanguageCode=language_code,
            MediaSampleRateHertz=sample_rate,
            MediaEncoding="pcm",
            # Additional settings can be added here
            # For example, PartialResultsStability="high", ContentIdentificationType="PII"
            # VocabularyName="my-custom-vocabulary", etc.
            # Refer to AWS Transcribe Streaming API documentation for full options.
            # https://docs.aws.amazon.com/transcribe/latest/dg/API_streaming_StartStreamTranscription.html
            EnablePartialResultsStabilization=True, # Enable interim transcripts
            PartialResultsStability="high"
        )

        async for event in response["ResponseStream"]:
            if "TranscriptEvent" in event:
                transcript = event["TranscriptEvent"]["Transcript"]
                if transcript and transcript["Results"]:
                    for result in transcript["Results"]:
                        if not result["IsPartial"]:
                            # Yield final results
                            yield result["Alternatives"][0]["Transcript"]
                        else:
                            # Yield interim results
                            yield result["Alternatives"][0]["Transcript"]

    except ClientError as e:
        print(f"AWS Transcribe streaming error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise

if __name__ == "__main__":
    async def main():
        print("Starting AWS Transcribe microphone stream...")
        async for transcript in stream_microphone_audio_aws():
            print(f"Transcript: {transcript}")
    asyncio.run(main())
