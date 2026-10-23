import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client, get_streaming_config

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


def stream_with_language_and_punctuation(
    language_code: str = "en-US", enable_punctuation: bool = True
):
    """Streams microphone audio with specified language and punctuation settings.

    Args:
        language_code: The BCP-47 language tag to use for recognition.
        enable_punctuation: Whether to enable automatic punctuation in the transcript.
    """
    client = get_speech_client()
    streaming_config = get_streaming_config(
        language_code=language_code, enable_automatic_punctuation=enable_punctuation
    )

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

    print(
        f"Listening with language '{language_code}' and punctuation '{enable_punctuation}'... Press Ctrl+C to stop."
    )

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
                if is_final:
                    print(f"Final ({language_code}): {transcript}")
                else:
                    print(f"Partial ({language_code}): {transcript}")

    finally:
        microphone_stream.stop_stream()
        microphone_stream.close()
        pyaudio.PyAudio().terminate()
