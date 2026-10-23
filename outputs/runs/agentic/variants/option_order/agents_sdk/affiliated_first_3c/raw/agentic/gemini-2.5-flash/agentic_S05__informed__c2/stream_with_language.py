import asyncio
import os
from google.cloud import speech

from stream_microphone import MicrophoneStream, RATE, CHUNK

async def stream_with_language_and_punctuation(
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    enable_word_time_offsets: bool = False,
):
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        enable_word_time_offsets=enable_word_time_offsets,
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    print(f"Starting streaming recognition with language='{language_code}', punctuation={enable_automatic_punctuation}...")
    print("Speak into the microphone.")

    async with MicrophoneStream(RATE, CHUNK) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            async for content in audio_generator
        )

        responses = client.streaming_recognize(config=streaming_config, requests=requests)

        try:
            async for response in responses:
                for result in response.results:
                    alternative = result.alternatives[0]
                    transcript = alternative.transcript

                    if result.is_final:
                        print(f"\nFinal ({language_code}): {transcript}")
                        if enable_word_time_offsets:
                            for word_info in alternative.words:
                                print(f"\tWord: {word_info.word}, Start: {word_info.start_time.seconds + word_info.start_time.nanos * 1e-9:.2f}s, End: {word_info.end_time.seconds + word_info.end_time.nanos * 1e-9:.2f}s")
                    else:
                        print(f"Interim ({language_code}): {transcript}\r", end="")

        except Exception as e:
            print(f"An error occurred during streaming: {e}")

if __name__ == "__main__":
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable.")
    else:
        try:
            # Example usage with French language and word time offsets
            asyncio.run(stream_with_language_and_punctuation(language_code="fr-FR", enable_word_time_offsets=True))
            # Example usage with English (default) and no punctuation
            # asyncio.run(stream_with_language_and_punctuation(enable_automatic_punctuation=False))
        except KeyboardInterrupt:
            print("\nStopping recognition.")
        except Exception as e:
            print(f"An error occurred: {e}")
