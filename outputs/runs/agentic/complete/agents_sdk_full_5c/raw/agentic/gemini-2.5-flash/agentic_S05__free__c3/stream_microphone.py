import asyncio
import pyaudio
from google.cloud import speech_v1p1beta1 as speech

from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig, RecognitionConfig, AudioEncoding, InterimResultsConfig

async def stream_microphone_audio(
    recognition_config: RecognitionConfig,
    interim_results_config: InterimResultsConfig
):
    client = get_speech_client()

    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16,
                    channels=1,
                    rate=recognition_config.sample_rate_hertz,
                    input=True,
                    frames_per_buffer=8192)

    streaming_config = speech.StreamingRecognitionConfig(
        config=speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding(recognition_config.encoding.value),
            sample_rate_hertz=recognition_config.sample_rate_hertz,
            language_code=recognition_config.language_code,
            enable_automatic_punctuation=recognition_config.enable_automatic_punctuation,
        ),
        interim_results=interim_results_config.interim_results,
    )

    async def request_generator():
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        while True:
            chunk = await asyncio.to_thread(stream.read, 8192)
            if not chunk:
                break
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(request_generator())

    async for response in responses:
        yield response

    stream.stop_stream()
    stream.close()
    p.terminate()
