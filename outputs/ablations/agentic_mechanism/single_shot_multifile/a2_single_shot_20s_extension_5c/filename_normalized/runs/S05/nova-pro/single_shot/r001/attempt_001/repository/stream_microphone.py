import pyaudio
import speech_client

def stream_microphone():
    client = speech_client.get_streaming_client()
    stream = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    stream.start_stream()
    while True:
        data = stream.read(1024)
        yield client.stream_audio(data)
    stream.stop_stream()
    stream.close()
