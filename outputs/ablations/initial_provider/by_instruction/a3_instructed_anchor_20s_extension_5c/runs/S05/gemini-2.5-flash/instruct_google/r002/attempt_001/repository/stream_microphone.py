import pyaudio
from google.cloud import speech_v1p1beta1 as speech

RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


def stream_microphone_audio():
    language_code = "en-US"

    client = speech.SpeechClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        # Google Speech-to-Text requires a model for streaming, specifying video as a common use case.
        model="video",
        # Enable automatic punctuation for better readability.
        enable_automatic_punctuation=True,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=True,
    )

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    print("* Listening...")

    requests = (
        speech.StreamingRecognizeRequest(audio_content=audio_chunk)
        for audio_chunk in generate_audio_chunks(stream)
    )

    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        yield response


def generate_audio_chunks(stream):
    while True:
        chunk = stream.read(CHUNK)
        yield chunk
