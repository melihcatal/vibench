import asyncio
from google.cloud import speech

# Google Cloud Speech-to-Text client setup
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
# or authenticate appropriately.

async def stream_audio_chunks(audio_chunk_generator):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True
    )

    # A generator that yields `speech.StreamingRecognizeRequest` objects
    async def request_generator():
        async for chunk in audio_chunk_generator:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    print("Starting Google Cloud Speech-to-Text streaming...")
    # The `stream_audio_chunks` function expects an async generator for audio chunks.
    # For example, this could be from a file reader, network stream, or another microphone input.
    responses = client.streaming_recognize(request_generator())

    try:
        for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            if result.is_final:
                yield {"final_transcript": transcript}
            else:
                yield {"interim_transcript": transcript}
    except Exception as e:
        print(f"Error during streaming: {e}")
        # Optionally re-raise or handle the error as appropriate

if __name__ == "__main__":
    # Example of a dummy async audio chunk generator
    async def dummy_audio_generator():
        for i in range(5):
            # Simulate sending empty bytes as audio data for demonstration
            await asyncio.sleep(1) # Simulate real-time audio chunks
            print(f"Sending dummy audio chunk {i+1}")
            yield b''
        print("Finished sending dummy audio chunks.")

    async def main():
        print("Google Cloud Speech-to-Text example will attempt to connect.")
        print("Please ensure you have authenticated with Google Cloud (e.g., gcloud auth application-default login)")
        print("and enabled the Speech-to-Text API.")
        async for transcript_data in stream_audio_chunks(dummy_audio_generator()):
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
