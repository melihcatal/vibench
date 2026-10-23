import time
from google.cloud.speech import StreamingRecognizeRequest
from speech_client import get_speech_client, get_streaming_config
from speech_models import CHUNK_SIZE, SAMPLE_RATE
import pyaudio

def microphone_stream():
    """A generator that yields audio chunks from the microphone."""
    audio_interface = pyaudio.PyAudio()
    stream = audio_interface.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
    )

    print("Listening... Press Ctrl+C to stop.")
    try:
        while True:
            data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
            yield data
    except KeyboardInterrupt:
        print("Stopping microphone stream.")
    finally:
        stream.stop_stream()
        stream.close()
        audio_interface.terminate()


def stream_from_mic():
    """Streams audio from the microphone and yields transcripts."""
    client = get_speech_client()
    streaming_config = get_streaming_config()

    audio_generator = microphone_stream()
    requests = (
        StreamingRecognizeRequest(audio_content=content)
        for content in audio_generator
    )

    # The streaming_recognize method returns a generator of responses
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

