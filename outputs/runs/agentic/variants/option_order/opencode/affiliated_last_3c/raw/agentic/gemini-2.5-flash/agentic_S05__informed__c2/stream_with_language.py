import pyaudio
from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client, get_streaming_config
from stream_microphone import generate_audio_chunks  # Re-using audio chunk generation

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


def start_streaming_recognizer(
    language_code="en-US", enable_automatic_punctuation=True
):
    client = get_speech_client()
    config = get_streaming_config(language_code, enable_automatic_punctuation)

    mic_manager = pyaudio.PyAudio()
    stream = mic_manager.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    requests = (
        speech.StreamingRecognizeRequest(audio_content=audio_chunk)
        for audio_chunk in generate_audio_chunks(stream)
    )

    responses = client.streaming_recognize(config=config, requests=requests)

    for response in responses:
        for result in response.results:
            if result.is_final:
                yield result.alternatives[0].transcript, True
            else:
                yield result.alternatives[0].transcript, False
