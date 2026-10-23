import asyncio
import pyaudio
from speech_client import SpeechClient
from speech_models import StreamingRecognitionConfig, SpeechRecognitionResult

# Google Cloud Speech-to-Text uses the `google.cloud.speech` SDK
# and `speech.SpeechClient` for its operations.


async def stream_microphone_audio(sample_rate: int = 16000, chunk_size: int = 1024):
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size,
    )

    print("Starting microphone stream...")

    async def generate_audio_chunks():
        while True:
            chunk = stream.read(chunk_size, exception_on_overflow=False)
            yield chunk

    config_params = StreamingRecognitionConfig(
        sample_rate_hertz=sample_rate, language_code="en-US", interim_results=True
    )
    speech_client = SpeechClient()

    try:
        async for response in speech_client.stream_audio_to_text(
            generate_audio_chunks(), config_params
        ):
            for result in response.results:
                if result.is_final:
                    print(f"Final: {result.alternatives[0].transcript}")
                else:
                    print(f"Interim: {result.alternatives[0].transcript}")
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
    # This part is for demonstration and requires `pyaudio` and `asyncio.run`.
    # In a real application, you'd integrate `stream_microphone_audio` into your async loop.
    try:
        # You might need to install `pyaudio` with `pip install PyAudio`
        # and potentially system-level audio libraries.
        async def main():
            async for transcript in stream_microphone_audio():
                # Process the results as they come in
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
