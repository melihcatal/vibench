import queue
import numpy as np
import sounddevice as sd
from google.cloud import speech
from speech_client import get_speech_client
from speech_models import get_streaming_config, SpeechResult

def generate_mic_audio():
    q = queue.Queue()
    sample_rate = 16000
    channels = 1
    blocksize = 3200

    def audio_callback(indata, frames, time, status):
        q.put(indata.tobytes())

    with sd.InputStream(samplerate=sample_rate, channels=channels, blocksize=blocksize, dtype=np.int16, callback=audio_callback):
        while True:
            data = q.get()
            yield data

def stream_with_language(language_code="es-ES", enable_punctuation=True):
    client = get_speech_client()
    streaming_config = get_streaming_config(
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
    )
    audio_generator = generate_mic_audio()
    requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in audio_generator)
    responses = client.streaming_recognize(streaming_config, requests)
    for response in responses:
        for result in response.results:
            yield SpeechResult(result.alternatives[0].transcript, result.is_final)
