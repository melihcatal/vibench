"""Stream microphone audio and yield interim transcripts using Google Cloud Speech-to-Text."""

import queue
import sys
import threading
import time

from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types as speech_types

import pyaudio
from speech_client import get_speech_client, build_streaming_config
from partial_results import handle_recognition_event

CHUNK_SIZE = 4096
SAMPLE_RATE = 16000
AUDIO_CHANNELS = 1
ENCODING = speech_types.RecognitionConfig.AudioEncoding.LINEAR16


def audio_generator(stop_event, audio_queue, timeout=0.1):
    """Generate audio chunks from the queue until stop_event is set."""
    while not stop_event.is_set():
        try:
            chunk = audio_queue.get(timeout=timeout)
            yield chunk
        except queue.Empty:
            continue


def stream_microphone_transcription(language_code="en-US", enable_punctuation=True, duration_limit=None):
    """Stream audio from the microphone and yield interim and final transcripts.

    Uses Google Cloud Speech-to-Text streaming recognition to process live audio input.

    Args:
        language_code: BCP-47 language code for recognition.
        enable_punctuation: Whether to enable automatic punctuation.
        duration_limit: Optional maximum streaming duration in seconds.

    Yields:
        Tuples of (transcript, is_final, confidence) from recognition events.
    """
    client = get_speech_client()
    config = build_streaming_config(
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
        encoding=ENCODING,
        sample_rate_hertz=SAMPLE_RATE,
    )

    audio_queue = queue.Queue()
    stop_event = threading.Event()

    def microphone_callback(in_data, frame_count, time_info, status):
        audio_queue.put(in_data)
        return (None, pyaudio.paContinue)

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=AUDIO_CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=CHUNK_SIZE,
        stream_callback=microphone_callback,
    )

    try:
        stream.start_stream()

        requests = (
            speech_types.StreamingRecognizeRequest(audio_content=chunk)
            for chunk in audio_generator(stop_event, audio_queue)
        )

        streaming_config = speech_types.StreamingRecognitionConfig(
            config=config,
            interim_results=True,
        )

        responses = client.streaming_recognize(
            config=streaming_config,
            requests=requests,
        )

        start_time = time.time()
        for response in responses:
            if duration_limit and (time.time() - start_time) >= duration_limit:
                break

            for result in response.results:
                for transcript, is_final, confidence in handle_recognition_event(result):
                    yield transcript, is_final, confidence

    finally:
        stop_event.set()
        stream.stop_stream()
        stream.close()
        audio.terminate()


if __name__ == "__main__":
    for transcript, is_final, confidence in stream_microphone_transcription():
        tag = "FINAL" if is_final else "INTERIM"
        print(f"[{tag}] (confidence={confidence:.2f}): {transcript}")
        sys.stdout.flush()
