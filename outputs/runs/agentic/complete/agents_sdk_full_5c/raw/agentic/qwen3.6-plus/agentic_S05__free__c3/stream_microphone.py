"""
Stream microphone audio and yield interim transcripts using Google Cloud Speech-to-Text.

Captures audio from a microphone device via PyAudio, streams it to the
google.cloud.speech.SpeechClient.streaming_recognize endpoint, and yields
interim transcript results as they are produced.
"""

import queue
import sys
from typing import Generator

from google.cloud import speech

from speech_client import create_speech_client, get_streaming_config, SpeechClientConfig
from speech_models import (
    StreamingAudioChunk,
    InterimTranscript,
    parse_streaming_response,
    build_initial_streaming_request,
    normalize_transcript_text,
)

SAMPLE_RATE = 16000
CHUNK_DURATION_MS = 500
BYTES_PER_SAMPLE = 2
CHANNELS = 1
FRAME_COUNT = int(SAMPLE_RATE * CHUNK_DURATION_MS / 1000)


def _audio_generator(
    audio_queue: queue.Queue, stop_event: object
) -> Generator[bytes, None, None]:
    """Generate audio chunks from a thread-safe queue for streaming."""
    while True:
        try:
            chunk = audio_queue.get(timeout=1)
            if chunk is None:
                break
            yield chunk
        except queue.Empty:
            continue


def stream_microphone(
    device_index: int | None = None,
    language_code: str = "en-US",
    enable_punctuation: bool = True,
) -> Generator[InterimTranscript, None, None]:
    """
    Stream live microphone audio to Google Cloud Speech-to-Text and yield interim transcripts.

    Uses PyAudio to capture audio from the default or specified microphone device,
    sends chunks to google.cloud.speech.SpeechClient.streaming_recognize,
    and yields InterimTranscript objects as recognition results arrive.

    Args:
        device_index: PyAudio device index (None for default).
        language_code: BCP-47 language code for recognition.
        enable_punctuation: Whether to enable automatic punctuation.

    Yields:
        InterimTranscript objects containing recognized text as audio is streamed.
    """
    import pyaudio

    config = SpeechClientConfig()
    client = create_speech_client(config)

    streaming_config = get_streaming_config(
        sample_rate_hertz=SAMPLE_RATE,
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
    )

    audio_queue: queue.Queue[bytes | None] = queue.Queue()
    stop_event = object()

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=CHANNELS,
        rate=SAMPLE_RATE,
        input=True,
        frames_per_buffer=FRAME_COUNT,
        input_device_index=device_index,
        stream_callback=_mic_callback_factory(audio_queue),
    )

    try:
        requests = _audio_generator(audio_queue, stop_event)
        initial_request = build_initial_streaming_request(streaming_config)

        request_iter = _prepend_initial_request(initial_request, requests)

        responses = client.streaming_recognize(
            config=streaming_config,
            requests=request_iter,
        )

        for response in responses:
            transcripts = parse_streaming_response(response)
            for transcript in transcripts:
                if isinstance(transcript, InterimTranscript):
                    transcript.text = normalize_transcript_text(transcript.text)
                    yield transcript
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        audio_queue.put(None)


def _mic_callback_factory(audio_queue: queue.Queue):
    """Create a PyAudio stream callback that pushes chunks into a queue."""

    def callback(in_data, frame_count, time_info, status):
        audio_queue.put(in_data)
        return (in_data, pyaudio.paContinue)

    return callback


def _prepend_initial_request(initial_request, request_iter):
    """Yield the initial config request first, then stream audio requests."""
    yield initial_request
    for audio_chunk in request_iter:
        yield speech.StreamingRecognizeRequest(audio_content=audio_chunk)
