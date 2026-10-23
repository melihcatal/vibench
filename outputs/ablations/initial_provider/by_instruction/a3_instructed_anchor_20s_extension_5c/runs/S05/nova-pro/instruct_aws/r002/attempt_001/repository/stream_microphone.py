import boto3
import wave
import pyaudio

def stream_microphone():
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    client = boto3.client('transcribe', region_name='us-west-2')
    stream.start_stream()
    try:
        while True:
            data = stream.read(1024)
            audio_chunk = {'AudioChunk': data}
            response = client.start_stream_transcription(
                LanguageCode='en-US',
                MediaEncoding='pcm',
                MediaSampleRateHertz=16000,
                **audio_chunk
            )
            yield response
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()