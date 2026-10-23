import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client, get_streaming_config

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


def stream_microphone_audio():
    """Streams audio from the microphone to Google Speech-to-Text and yields transcripts."""
    client = get_speech_client()
    streaming_config = get_streaming_config()

    # In rare cases, if the stream is not closed properly, a ResourceExhausted error might occur.
    # It's recommended to handle stream closure gracefully in a real-world application.
    microphone_stream = pyaudio.PyAudio().open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    def request_generator():
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        while True:
            chunk = microphone_stream.read(CHUNK)
            if not chunk:
                break
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    try:
        responses = client.streaming_recognize(request_generator())

        for response in responses:
            if not response.results:
                continue

            for result in response.results:
                if not result.alternatives:
                    continue

                transcript = result.alternatives[0].transcript
                is_final = result.is_final
                yield transcript, is_final

    finally:
        microphone_stream.stop_stream()
        microphone_stream.close()
        pyaudio.PyAudio().terminate()
