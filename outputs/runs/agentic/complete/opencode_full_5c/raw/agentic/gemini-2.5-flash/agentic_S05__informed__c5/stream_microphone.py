import os
import io
from google.cloud import speech


def stream_microphone_audio():
    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    # In a real scenario, this would interface with an actual microphone.
    # For demonstration, we'll simulate an audio input.
    # Replace this with actual microphone input (e.g., using PyAudio)
    def audio_generator():
        yield b"simulated_audio_chunk_1"
        yield b"simulated_audio_chunk_2"
        # In a real application, you would read audio from the microphone
        # For example:
        # import pyaudio
        # audio = pyaudio.PyAudio()
        # stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
        # while True:
        #     yield stream.read(1024)

    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in audio_generator()
    )
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        for result in response.results:
            yield result.alternatives[0].transcript
