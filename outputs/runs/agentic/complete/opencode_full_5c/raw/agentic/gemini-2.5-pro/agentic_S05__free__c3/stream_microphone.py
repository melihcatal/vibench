import sounddevice as sd
import numpy as np
from speech_client import get_speech_client, get_streaming_config
from google.cloud.speech_v1.types import StreamingRecognizeRequest
import queue

RATE = 16000
CHUNK = int(RATE / 10)


def stream_microphone():
    audio_queue = queue.Queue()

    def audio_callback(indata, frames, time, status):
        if status:
            print(status)
        audio_queue.put(bytes(indata))

    client = get_speech_client()
    streaming_config = get_streaming_config(rate=RATE)

    with sd.RawInputStream(
        samplerate=RATE,
        blocksize=CHUNK,
        dtype="int16",
        channels=1,
        callback=audio_callback,
    ) as device:
        print("Listening...")

        audio_generator = (
            audio_queue.get() for _ in range(int(5 * RATE / CHUNK))
        )  # 5 seconds of audio

        requests = (
            StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        streaming_recognize_rpc = client.streaming_recognize(
            config=streaming_config, requests=requests
        )

        for response in streaming_recognize_rpc:
            for result in response.results:
                if result.alternatives:
                    print(f"Interim transcript: {result.alternatives[0].transcript}")


if __name__ == "__main__":
    stream_microphone()
