import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPIError

from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig, StreamingRecognitionResponse

def stream_microphone_audio(
    rate: int = 16000,
    chunk_size: int = 1024
) -> StreamingRecognitionResponse:
    """Streams audio from the microphone and yields interim transcripts."""

    client = get_speech_client()

    audio_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=rate,
        language_code="en-US",
    )
    streaming_config = StreamingRecognitionConfig(config=audio_config, interim_results=True)

    mic_audio = pyaudio.PyAudio()
    mic_stream = mic_audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=rate,
        input=True,
        frames_per_buffer=chunk_size
    )

    def generate_requests():
        yield streaming_config.to_proto()
        while True:
            chunk = mic_stream.read(chunk_size)
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    try:
        responses = client.streaming_recognize(generate_requests())
        for response in responses:
            yield StreamingRecognitionResponse.from_proto(response)
    except GoogleAPIError as e:
        print(f"Google Cloud Speech-to-Text API Error: {e}")
    finally:
        mic_stream.stop_stream()
        mic_stream.close()
        mic_audio.terminate()
