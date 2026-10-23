import asyncio
import os
from google.cloud import speech

# This example reuses the microphone stream for simplicity.
# In a real application, this could be any source of audio chunks.
from stream_microphone import MicrophoneStream, RATE, CHUNK

async def handle_partial_and_final_results(language_code: str = "en-US"):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True, # Essential for partial results
    )

    print("Starting streaming recognition to handle partial and final results...")
    print("Speak into the microphone. Interim results will update, final results will be marked.")

    async with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            async for content in audio_generator
        )

        responses = client.streaming_recognize(config=streaming_config, requests=requests)

        try:
            async for response in responses:
                # Iterate through results received from the API.
                for result in response.results:
                    # The alternatives are ordered from most likely to least likely.
                    alternative = result.alternatives[0]
                    transcript = alternative.transcript

                    if result.is_final:
                        print(f"\nFinal Result: {transcript} (Confidence: {alternative.confidence:.2f})\n")
                    else:
                        # Interim results may change, so overwrite the line in the console.
                        # Using `\r` to return to the start of the line.
                        print(f"Interim Result: {transcript}\r", end="")

        except Exception as e:
            print(f"An error occurred during streaming: {e}")

if __name__ == "__main__":
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable.")
    else:
        try:
            asyncio.run(handle_partial_and_final_results())
        except KeyboardInterrupt:
            print("\nStopping recognition.")
        except Exception as e:
            print(f"An error occurred: {e}")
