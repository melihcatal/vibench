import asyncio
import pyaudio
from speech_client import SpeechClient
from speech_models import StreamingRecognitionConfig, SpeechRecognitionResult

# Google Cloud Speech-to-Text uses the `google.cloud.speech` SDK
# and `speech.SpeechClient` for its operations.


async def stream_with_language_and_punctuation(
    sample_rate: int = 16000,
    chunk_size: int = 1024,
    language_code: str = "es-ES",  # Example: Spanish
    enable_automatic_punctuation: bool = True,
):
    """
    Streams microphone audio with specified language and punctuation settings
    to Google Cloud Speech-to-Text and yields interim transcripts.

    Args:
        sample_rate: The sample rate of the audio.
        chunk_size: The size of audio chunks to process.
        language_code: The BCP-47 language tag for the recognition (e.g., "en-US", "es-ES").
        enable_automatic_punctuation: Whether to enable automatic punctuation.

    Yields:
        SpeechRecognitionResult: Interim or final transcription results.
    """
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size,
    )

    print(
        f"Starting microphone stream with language: {language_code} and punctuation: {enable_automatic_punctuation}..."
    )

    async def generate_audio_chunks():
        while True:
            chunk = stream.read(chunk_size, exception_on_overflow=False)
            yield chunk

    config_params = StreamingRecognitionConfig(
        sample_rate_hertz=sample_rate,
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        interim_results=True,
    )
    speech_client = SpeechClient()

    try:
        async for response in speech_client.stream_audio_to_text(
            generate_audio_chunks(), config_params
        ):
            for result in response.results:
                if result.is_final:
                    print(
                        f"Final ({language_code}): {result.alternatives[0].transcript}"
                    )
                else:
                    print(
                        f"Interim ({language_code}): {result.alternatives[0].transcript}"
                    )
                yield SpeechRecognitionResult(
                    transcript=result.alternatives[0].transcript,
                    is_final=result.is_final,
                    confidence=result.alternatives[0].confidence,
                )
    except Exception as e:
        print(f"Error during streaming: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        print("Microphone stream stopped.")


if __name__ == "__main__":
    try:

        async def main():
            async for transcript in stream_with_language_and_punctuation(
                language_code="fr-FR", enable_automatic_punctuation=True
            ):
                pass

        asyncio.run(main())
    except ImportError:
        print(
            "PyAudio not found. Please install it to run the microphone streaming example."
        )
        print(
            "On macOS, you might need `brew install portaudio && pip install pyaudio`"
        )
    except Exception as e:
        print(f"An error occurred: {e}")
