import pyaudio
from google.cloud import speech
from speech_client import get_speech_client, RATE, CHUNK

def stream_microphone():
    """Streams audio from the microphone and yields transcripts from the Speech-to-Text API."""
    client = get_speech_client()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    audio_interface = pyaudio.PyAudio()
    audio_stream = audio_interface.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print("Listening...")

    def audio_generator():
        while True:
            try:
                data = audio_stream.read(CHUNK, exception_on_overflow=False)
                if not data:
                    break
                yield speech.StreamingRecognizeRequest(audio_content=data)
            except IOError:
                # Can happen if the stream is closed
                break
    
    requests = audio_generator()
    responses = client.streaming_recognize(streaming_config, requests)

    try:
        for response in responses:
            yield response
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        audio_interface.terminate()
