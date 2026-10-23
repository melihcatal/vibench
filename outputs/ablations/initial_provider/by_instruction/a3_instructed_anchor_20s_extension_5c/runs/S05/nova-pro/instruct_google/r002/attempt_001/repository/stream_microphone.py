import pyaudio
import time

from speech_client import speech_client

# Stream microphone audio and yield interim transcripts
def stream_microphone():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                     channels=1,
                     rate=16000,
                     input=True,
                     frames_per_buffer=1024)
    stream.start_stream()
    while stream.is_active():
        audio_content = stream.read(1024)
        yield audio_content
    stream.stop_stream()
    stream.close()
    p.terminate()