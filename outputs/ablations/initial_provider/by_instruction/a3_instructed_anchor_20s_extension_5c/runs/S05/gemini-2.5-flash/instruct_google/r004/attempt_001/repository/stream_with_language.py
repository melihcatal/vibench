from google.cloud import speech
from speech_client import SpeechClient
from speech_models import StreamingRecognitionConfig
import sounddevice as sd

def stream_with_language_settings(language_code: str, enable_automatic_punctuation: bool):
    config = StreamingRecognitionConfig(
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )
    client = SpeechClient()
    streaming_config = client.get_streaming_config(config)

    samplerate = config.sample_rate_hertz
    blocksize = 16000
    channels = 1

    def generator():
        with sd.RawInputStream(
            samplerate=samplerate,
            blocksize=blocksize,
            dtype='int16',
            channels=channels,
        ) as stream:
            while True:
                data, overflowed = stream.read(blocksize)
                if overflowed:
                    print("Audio overflowed")
                yield data.tobytes()

    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in generator())

    responses = client.client.streaming_recognize(streaming_config, requests)

    for response in responses:
        yield response
