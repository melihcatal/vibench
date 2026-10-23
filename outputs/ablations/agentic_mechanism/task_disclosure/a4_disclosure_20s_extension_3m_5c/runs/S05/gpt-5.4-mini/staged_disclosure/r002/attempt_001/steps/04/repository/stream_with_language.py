import os
import sys
import threading

import pyaudio
from deepgram import DeepgramClient, LiveOptions, LiveTranscriptionEvents


def main():
    api_key = os.getenv("DEEPGRAM_API_KEY")
    if not api_key:
        raise RuntimeError("DEEPGRAM_API_KEY is required")

    language = os.getenv("TRANSCRIPTION_LANGUAGE", "en-US")
    sample_rate = int(os.getenv("AUDIO_SAMPLE_RATE", "16000"))
    channels = 1
    chunk_size = 1024

    client = DeepgramClient(api_key)
    connection = client.listen.live.v("1")

    done = threading.Event()

    def on_open(_, __, ***kwargs):
        pass

    def on_transcript(_, result, **kwargs):
        alt = result.channel.alternatives[0]
        transcript = alt.transcript.strip()
        if transcript:
            print(transcript)

    def on_error(_, error, **kwargs):
        print(error, file=sys.stderr)

    def on_close(_, **kwargs):
        done.set()

    connection.on(LiveTranscriptionEvents.Open, on_open)
    connection.on(LiveTranscriptionEvents.Transcript, on_transcript)
    connection.on(LiveTranscriptionEvents.Error, on_error)
    connection.on(LiveTranscriptionEvents.Close, on_close)

    options = LiveOptions(
        model="nova-2",
        language=language,
        punctuate=True,
        interim_results=True,
        smart_format=True,
        encoding="linear16",
        sample_rate=sample_rate,
        channels=channels,
    )

    connection.start(options)

    pa = pyaudio.PyAudio()
    stream = pa.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=chunk_size,
    )

    try:
        while not done.is_set():
            data = stream.read(chunk_size, exception_on_overflow=False)
            connection.send(data)
    except KeyboardInterrupt:
        pass
    finally:
        try:
            connection.finish()
        finally:
            stream.stop_stream()
            stream.close()
            pa.terminate()


if __name__ == "__main__":
    main()
