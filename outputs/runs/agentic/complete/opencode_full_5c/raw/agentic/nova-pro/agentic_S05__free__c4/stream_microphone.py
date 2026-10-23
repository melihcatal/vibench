import pyaudio
import time
from speech_client import create_streaming_recognizer


def stream_microphone():
    client, streaming_config = create_streaming_recognizer()
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 16000
    chunk = 1024
    audio_interface = pyaudio.PyAudio()
    stream = audio_interface.open(
        format=audio_format,
        channels=channels,
        rate=rate,
        input=True,
        frames_per_buffer=chunk,
    )
    print("Streaming started...")
    while True:
        audio_data = stream.read(chunk)
        audio = types.RecognitionAudio(content=audio_data)
        request = types.StreamingRecognizeRequest(audio_content=audio.content)
        responses = client.streaming_recognize(streaming_config, [request])
        for response in responses:
            for result in response.results:
                print("Transcript: {}".format(result.alternatives[0].transcript))
    stream.stop_stream()
    stream.close()
    audio_interface.terminate()
