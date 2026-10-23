import pyaudio
from google.cloud import speech_v1p1beta1 as speech
import os

from speech_client import get_speech_client
from speech_models import RecognitionConfig, StreamingRecognitionConfig

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms chunks


def stream_microphone_audio(language_code: str = "en-US"):
    """
    Streams microphone audio to Google Cloud Speech-to-Text and yields interim transcripts.
    """
    client = get_speech_client()

    # Configure the streaming request
    recognition_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
    )

    # Generator that yields audio chunks from the microphone
    def generate_audio_chunks():
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
        )

        print("Listening... Press Ctrl+C to stop.")
        try:
            while True:
                data = stream.read(CHUNK)
                yield data
        except KeyboardInterrupt:
            pass
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

    # Stream audio to Google Cloud Speech-to-Text
    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in generate_audio_chunks()
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
            yield f"Final: {transcript}"
        else:
            yield f"Interim: {transcript}"


if __name__ == "__main__":
    # Example usage: Ensure GOOGLE_APPLICATION_CREDENTIALS is set
    # For real use, consider running this in an async loop or separate thread
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable.")
    else:
        try:
            for transcript in stream_microphone_audio():
                print(transcript)
        except Exception as e:
            print(f"An error occurred: {e}")
