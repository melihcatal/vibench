import pyaudio
import time
from speech_client import create_speech_client
from speech_models import create_streaming_config

def stream_microphone():
    client = create_speech_client()
    config = create_streaming_config(language_code='en-US', enable_automatic_punctuation=True)
    audio_format = pyaudio.paInt16
    channels = 1
    rate = 16000
    chunk_size = 1024
    audio_interface = pyaudio.PyAudio()
    stream = audio_interface.open(format=audio_format,
                                  channels=channels,
                                  rate=rate,
                                  input=True,
                                  frames_per_buffer=chunk_size)
    print('Streaming started. Speak into the microphone.')
    while True:
        audio_content = stream.read(chunk_size)
        if len(audio_content) == 0:
            break
        audio = types.RecognitionAudio(content=audio_content)
        request = types.StreamingRecognizeRequest(audio_content=audio)
        responses = client.streaming_recognize(config=config, requests=[request])
        for response in responses:
            for result in response.results:
                print('Transcript: {}'.format(result.alternatives[0].transcript))
    stream.stop_stream()
    stream.close()
    audio_interface.terminate()