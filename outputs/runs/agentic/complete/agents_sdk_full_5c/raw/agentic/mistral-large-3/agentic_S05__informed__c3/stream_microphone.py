import os
import pyaudio
from speech_client import get_deepgram_client
from partial_results import handle_partial_result

def stream_microphone():
    client = get_deepgram_client()
    deepgram_socket = client.listen.live.v("latest")

    def on_message(ws, message):
        handle_partial_result(message)

    deepgram_socket.registerHandler(deepgram_socket.event.CLOSE, lambda _: print("Deepgram connection closed"))
    deepgram_socket.registerHandler(deepgram_socket.event.MESSAGE, on_message)

    audio = pyaudio.PyAudio()
    stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()

    try:
        while True:
            data = stream.read(4096, exception_on_overflow=False)
            deepgram_socket.send(data)
    except KeyboardInterrupt:
        stream.stop_stream()
        stream.close()
        audio.terminate()
        deepgram_socket.finish()