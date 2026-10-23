import asyncio
import boto3
import json
import os

# AWS Transcribe client setup
# Ensure AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN) 
# are set as environment variables or configured via AWS CLI.

# AWS Region - change as needed
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

async def stream_with_language(audio_stream_generator, language_code="en-US", enable_partial_results_stabilization=True, pii_entity_types=None):
    if not os.getenv("AWS_ACCESS_KEY_ID") or not os.getenv("AWS_SECRET_ACCESS_KEY"):
        print("WARNING: AWS credentials are not set. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables.")
        # In a real application, you might raise an error or exit.
        # For this example, we will proceed but it will fail if credentials are truly missing.

    client = boto3.client("transcribe", region_name=AWS_REGION)

    # This is a helper function to convert the audio chunks into the format expected by Transcribe
    async def audio_stream():
        async for chunk in audio_stream_generator:
            yield {"AudioEvent": {"AudioChunk": chunk}}

    print(f"Starting AWS Transcribe streaming for language: {language_code}...")

    try:
        response = client.start_stream_transcription(
            LanguageCode=language_code,
            MediaSampleRateHertz=16000,
            MediaEncoding="pcm", # raw PCM audio
            # For a truly real-time application, enable interim results
            # Transcribe does not have an explicit `interim_results` flag like GCP,
            # but it sends back results as soon as it has them.
            EnablePartialResultsStabilization=enable_partial_results_stabilization,
            # If you want to identify PII, you would set this:
            # PIIEntityTypes="BANK_ACCOUNT_NUMBER,CREDIT_CARD_NUMBER,EMAIL,NAME,PHONE_NUMBER,SSN",
            # ContentIdentificationType="PII",
            # ContentRedactionType="PII",
            # PIIEntityTypes=pii_entity_types if pii_entity_types else [],
            AudioStream=audio_stream()
        )

        async for event in response["TranscriptResultStream"]:
            if "TranscriptEvent" in event:
                for result in event["TranscriptEvent"]["Results"]:
                    if not result["IsPartial"] and result["Alternatives"]:
                        yield {"final_transcript": result["Alternatives"][0]["Transcript"]}
                    elif result["IsPartial"] and result["Alternatives"]:
                        yield {"interim_transcript": result["Alternatives"][0]["Transcript"]}

    except Exception as e:
        print(f"Error during AWS Transcribe streaming: {e}")
        # Optionally re-raise or handle the error

if __name__ == "__main__":
    async def dummy_audio_input_generator():
        print("Starting dummy audio input generation for AWS Transcribe...")
        for i in range(5):
            await asyncio.sleep(1) # Simulate real-time audio chunks
            print(f"Sending dummy audio chunk {i+1}")
            # Sending empty bytes for demonstration. In a real app, send actual audio.
            # AWS Transcribe expects raw PCM audio, 16-bit, 16kHz mono. 
            # An empty chunk might cause issues, so providing a small dummy byte string.
            yield b'\x00' * 3200 # Roughly 0.1 seconds of silent audio at 16kHz, 16-bit mono
        print("Dummy audio input generation finished.")

    async def main():
        print("AWS Transcribe streaming example will attempt to connect.")
        print("Please ensure your AWS credentials are set as environment variables (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY).")
        async for transcript_data in stream_with_language(
            dummy_audio_input_generator(),
            language_code="en-US",
            enable_partial_results_stabilization=True
        ):
            if "interim_transcript" in transcript_data:
                print(f"Interim: {transcript_data['interim_transcript']}")
            elif "final_transcript" in transcript_data:
                print(f"Final: {transcript_data['final_transcript']}")

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Streaming stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")
