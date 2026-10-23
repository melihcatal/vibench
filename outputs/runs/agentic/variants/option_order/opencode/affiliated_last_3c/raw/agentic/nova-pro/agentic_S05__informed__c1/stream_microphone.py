import pyaudio
import wave
import json

from speech_client import speech_to_text


def stream_microphone():
    # Set up the audio recording
    chunk = 1024
    format = pyaudio.paInt16
    channels = 1
    rate = 44100
    p = pyaudio.PyAudio()
    stream = p.open(
        format=format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk
    )
    print("Start speaking.")
    frames = []
    # Stream the audio to the Speech-to-Text service
    with speech_to_text.get_websocket(content_type="audio/l16;rate=44100") as websocket:
        while websocket.is_open():
            data = stream.read(chunk)
            frames.append(data)
            websocket.send(data)
            result = websocket.receive()
            if result["results"][0]["is_final"]:
                print(result["results"][0]["alternatives"][0]["transcript"])
    stream.stop_stream()
    stream.close()
    p.terminate()
