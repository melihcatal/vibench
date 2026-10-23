import time
from google.cloud import speech
from speech_client import get_speech_client

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


def stream_microphone():
    """Streams audio from the microphone and yields transcripts."""
    client = get_speech_client()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    try:
        import sounddevice as sd

        with sd.InputStream(samplerate=RATE, channels=1, blocksize=CHUNK) as stream:
            audio_generator = (
                speech.StreamingRecognizeRequest(audio_content=content)
                for content, _ in stream
            )

            requests = (
                speech.StreamingRecognizeRequest(audio_content=bytes(content))
                for content, status in stream
            )

            responses = client.streaming_recognize(streaming_config, requests)

            for response in responses:
                if not response.results:
                    continue

                result = response.results[0]
                if not result.alternatives:
                    continue

                transcript = result.alternatives[0].transcript

                if result.is_final:
                    yield f"Final transcript: {transcript}"
                else:
                    yield f"Interim transcript: {transcript}"

    except ImportError:
        print("Please install sounddevice: pip install sounddevice")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    for transcript in stream_microphone():
        print(transcript)
        # Add a small delay to simulate real-time processing
        time.sleep(0.1)
