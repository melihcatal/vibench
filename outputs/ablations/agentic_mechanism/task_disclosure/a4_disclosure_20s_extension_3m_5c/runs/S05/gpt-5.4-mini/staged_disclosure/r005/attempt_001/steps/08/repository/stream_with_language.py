import os
import queue
import sys

import sounddevice as sd
from google.cloud import speech


RATE = 16000
CHUNK = int(RATE / 10)


def main() -> None:
    language_code = os.getenv("GOOGLE_SPEECH_LANGUAGE_CODE", "en-US")
    enable_punctuation = os.getenv("GOOGLE_SPEECH_ENABLE_PUNCTUATION", "1") not in {"0", "false", "False"}

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
        model=os.getenv("GOOGLE_SPEECH_MODEL", "latest_long"),
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
        single_utterance=False,
    )

    audio_queue: queue.Queue[bytes] = queue.Queue()

    def callback(indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        audio_queue.put(bytes(indata))

    def request_stream():
        while True:
            chunk = audio_queue.get()
            if chunk is None:
                return
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    with sd.RawInputStream(
        samplerate=RATE,
        blocksize=CHUNK,
        dtype="int16",
        channels=1,
        callback=callback,
    ):
        requests = request_stream()
        responses = client.streaming_recognize(streaming_config, requests)
        for response in responses:
            for result in response.results:
                if not result.alternatives:
                    continue
                transcript = result.alternatives[0].transcript
                if result.is_final:
                    print(transcript)
                else:
                    print(transcript, end="\r", flush=True)


if __name__ == "__main__":
    main()
