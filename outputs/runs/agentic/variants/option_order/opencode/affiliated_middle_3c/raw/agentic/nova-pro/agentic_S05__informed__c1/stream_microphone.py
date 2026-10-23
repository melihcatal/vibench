import pyaudio
import wave
import json

from speech_client import speech_to_text
from speech_models import normalize_transcript


def stream_microphone():
    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=44100,
        input=True,
        frames_per_buffer=1024,
    )
    stream.start_stream()
    with speech_to_text.create_session() as session:
        while stream.is_active():
            audio_data = stream.read(1024)
            results = session.send_audio(audio_data)
            transcript = normalize_transcript(results)
            yield transcript
    stream.stop_stream()
    stream.close()
    p.terminate()
