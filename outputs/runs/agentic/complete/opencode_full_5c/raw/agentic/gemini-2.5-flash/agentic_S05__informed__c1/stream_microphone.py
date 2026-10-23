import os
from speech_client import get_speech_client
from speech_models import get_streaming_config


# Mocking pyaudio for demonstration purposes
class MockPyAudio:
    def open(self, *args, **kwargs):
        return self

    def read(self, *args, **kwargs):
        # Return empty bytes to simulate no audio or end of stream
        return b""

    def close(self):
        pass

    def terminate(self):
        pass


# Replace this with actual PyAudio import if running in an environment with microphone access
try:
    import pyaudio

    AUDIO = pyaudio.PyAudio()
except ImportError:
    print(
        "pyaudio not found, using mock PyAudio. Microphone streaming will not be functional."
    )
    AUDIO = MockPyAudio()

RATE = 16000
CHUNK = int(RATE / 10)  # 100ms chunks


def stream_microphone_audio():
    """
    Streams audio from the microphone and yields interim transcripts.
    """
    client = get_speech_client()
    streaming_config = get_streaming_config()

    # Mock audio stream for demonstration
    # In a real scenario, this would be an actual PyAudio stream
    microphone_stream = AUDIO.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    def generate_requests():
        while True:
            data = microphone_stream.read(CHUNK)
            if not data:
                break
            yield speech.StreamingRecognizeRequest(audio_content=data)

    print("Listening... Press Ctrl+C to stop.")
    requests = generate_requests()
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        if not response.results:
            continue

        result = response.results[0]
        if not result.alternatives:
            continue

        transcript = result.alternatives[0].transcript
        if result.is_final:
            print(f"Final: {transcript}")
        else:
            print(f"Interim: {transcript}")
        yield transcript

    microphone_stream.close()
    AUDIO.terminate()


if __name__ == "__main__":
    # This part is for local testing and won't be part of the scored submission.
    # try:
    #     for transcript in stream_microphone_audio():
    #         pass
    # except KeyboardInterrupt:
    #     print("\nStopped listening.")
    pass
