import asyncio
import os
import wave

import boto3
from botocore.exceptions import ClientError


class MicrophoneStream:
    """
    Audio stream from the microphone to AWS Transcribe.
    """

    def __init__(self, client, language_code="en-US", sample_rate=16000, channels=1):
        self._client = client
        self._language_code = language_code
        self._sample_rate = sample_rate
        self._channels = channels
        self._stream_id = None

    async def _send_audio_stream(self, audio_data_producer):
        try:
            # Start transcription stream
            response = await self._client.start_stream_transcription(
                LanguageCode=self._language_code,
                MediaSampleRateHertz=self._sample_rate,
                MediaEncoding="pcm",
                # The AWS Transcribe model to use. 'transcribe' is the default and general purpose.
                # For specific use cases, consider 'medical' or 'call_analytics'.
                # For a broader range of models, refer to AWS Transcribe documentation.
                # The model type is automatically selected by AWS based on language and sample rate,
                # but you can specify 'model_name' if needed for advanced configurations.
                # Using 'IdentifyLanguage' for automatic language detection.
                # In a real-world scenario, you might have a pre-selected language.
                # Using a general purpose model, often identified as 'en-US', as an example.
                # This could be adapted to 'en-AU', 'en-GB', etc. for specific English variants.
                # For example, to use a specific model:
                # ModelName="chime", # or "telephony", etc.
                # Using the default model implies a balance of accuracy and latency for general speech.
                # For a more specific model, one would specify its name like "medical" or "legal".
                # AWS Transcribe typically infers the model from language and sample rate.
                # The code here assumes the default model for 'en-US'.
                # You can find more details in AWS Transcribe Developer Guide.
                # For instance, the 'general' model for 'en-US' might be 'en-US_General_V2'.
                # The client automatically handles the session management for streaming.
                # The content identification can be for language or for a custom vocabulary.
                # Here, a general approach is taken for the example.
                # The actual model used is dependent on the service and region.
                # For better control, use 'model_name'.
                # For instance: ModelName="medical", Specialty="PRIMARYCARE"
                # If using a custom vocabulary: VocabularyName="MyCustomVocab"
                # If using a custom language model: LanguageModelName="MyCustomLanguageModel"
                # For this example, we rely on automatic model selection for the specified language and encoding.
            )

            self._stream_id = response["ResponseMetadata"]["RequestId"]
            print(f"AWS Transcribe stream started with ID: {self._stream_id}")

            async for chunk in audio_data_producer():
                await response.request_body.send_all(chunk)
            await response.request_body.send_eof()

            full_transcript = []
            async for event in response.async_iterator():
                if "TranscriptEvent" in event:
                    transcript = event["TranscriptEvent"]
                    for result in transcript["Results"]:
                        if not result["IsPartial"]:
                            text = " ".join([alt["Content"] for alt in result["Alternatives"]])
                            full_transcript.append(text)
                            yield {"type": "final", "text": text}
                        else:
                            text = " ".join([alt["Content"] for alt in result["Alternatives"]])
                            yield {"type": "interim", "text": text}
            print("Full transcript: " + " ".join(full_transcript))

        except ClientError as e:
            print(f"AWS Transcribe client error: {e}")
            raise
        except Exception as e:
            print(f"Error during AWS Transcribe streaming: {e}")
            raise

    async def generate_transcripts(self, audio_data_producer):
        async for transcript_event in self._send_audio_stream(audio_data_producer):
            yield transcript_event

# Example of how you might use this with a dummy audio producer (e.g., from a file or microphone)
async def dummy_audio_producer():
    # In a real scenario, this would read from a microphone or an audio file
    # For demonstration, we'll use a silent audio chunk.
    # Replace with actual audio input
    dummy_audio_chunk = b'\x00' * 3200  # 16kHz, 16-bit, 1 channel, 100ms of silence
    for _ in range(10):  # Simulate 1 second of audio
        yield dummy_audio_chunk
        await asyncio.sleep(0.1)

async def main():
    # Configure AWS Transcribe client
    # Ensure AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY are set as environment variables
    # or configured via AWS CLI.
    try:
        aws_region = os.environ.get("AWS_REGION", "us-east-1") # Example region
        aws_client = boto3.client("transcribe", region_name=aws_region)
        
        # Using the async client for streaming
        # Note: Boto3's default client is synchronous. For async operations,
        # you might need to use aiobotocore or a similar async wrapper,
        # or handle async execution with threads.
        # For simplicity and demonstrating the interface, this example assumes
        # an async-compatible client or a wrapper for 'start_stream_transcription'.
        # In a full async application, 'aiobotocore' would be used:
        # from aiobotocore.session import get_session
        # session = get_session()
        # async with session.client("transcribe", region_name=aws_region) as client:
        #    streamer = MicrophoneStream(client)
        #    async for transcript in streamer.generate_transcripts(dummy_audio_producer):
        #        print(transcript)
        
        # For this example, we will simulate an async client by using the synchronous
        # client within an asyncio context. A real async implementation would use aiobotocore.
        class AsyncTranscribeClient:
            def __init__(self, sync_client):
                self._sync_client = sync_client

            async def start_stream_transcription(self, **kwargs):
                # This is a simplification. In a real async app, this would use aiobotocore.
                # For this example, we're returning a mock stream object.
                print("Simulating start_stream_transcription call...")
                return MockAWSStreamResponse()

        class MockAWSStreamResponse:
            def __init__(self):
                self.request_body = MockRequestBody()
                self._async_iterator = self._generate_mock_events()
                self.ResponseMetadata = {"RequestId": "mock-stream-id-123"}

            async def _generate_mock_events(self):
                # Simulate a few interim and a final transcript event
                yield {
                    "TranscriptEvent": {
                        "Results": [
                            {"IsPartial": True, "Alternatives": [{"Content": "hello"}]}
                        ]
                    }
                }
                await asyncio.sleep(0.5)
                yield {
                    "TranscriptEvent": {
                        "Results": [
                            {"IsPartial": True, "Alternatives": [{"Content": "hello world"}]}
                        ]
                    }
                }
                await asyncio.sleep(0.5)
                yield {
                    "TranscriptEvent": {
                        "Results": [
                            {"IsPartial": False, "Alternatives": [{"Content": "Hello world this is a test"}]}
                        ]
                    }
                }

            def async_iterator(self):
                return self._async_iterator

        class MockRequestBody:
            async def send_all(self, chunk):
                # print(f"MockRequestBody received chunk of size: {len(chunk)}")
                pass

            async def send_eof(self):
                print("MockRequestBody sent EOF")

        async_aws_client = AsyncTranscribeClient(aws_client)
        
        streamer = MicrophoneStream(async_aws_client)
        async for transcript in streamer.generate_transcripts(dummy_audio_producer):
            print(f"Received transcript event: {transcript}")

    except Exception as e:
        print(f"An error occurred in main: {e}")

if __name__ == "__main__":
    asyncio.run(main())
