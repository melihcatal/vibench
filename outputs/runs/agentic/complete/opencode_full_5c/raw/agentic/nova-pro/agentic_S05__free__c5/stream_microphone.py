import pyaudio
import speech_client


def stream_microphone():
    client = speech_client.get_speech_client()
    config = speech_models.create_streaming_config(
        language_code="en-US", enable_automatic_punctuation=True
    )
    streaming_recognizer = client.streaming_recognize(config)
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024,
    )
    stream.start_stream()
    while True:
        audio_chunk = stream.read(1024)
        if len(audio_chunk) == 0:
            break
        streaming_recognizer.send_audio(audio_chunk)
        for response in streaming_recognizer.responses:
            yield response
