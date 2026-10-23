import pyaudio
from google.cloud import speech
from speech_client import get_speech_client

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


def stream_with_language_and_punctuation(
    language_code: str = "en-US", enable_punctuation: bool = True
):
    client = get_speech_client()

    audio_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=language_code,
        enable_automatic_punctuation=enable_punctuation,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=audio_config,
        interim_results=True,
    )

    mic_stream = pyaudio.PyAudio()
    stream = mic_stream.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
    )

    def request_generator():
        while True:
            chunk = stream.read(CHUNK)
            if not chunk:
                break
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    print(
        f"Listening with language {language_code} and punctuation {enable_punctuation}... Press Ctrl+C to stop."
    )
    requests = request_generator()
    responses = client.streaming_recognize(streaming_config, requests)

    try:
        for response in responses:
            if not response.results:
                continue

            result = response.results[0]
            if not result.alternatives:
                continue

            transcript = result.alternatives[0].transcript
            yield {"is_final": result.is_final, "transcript": transcript}
    except KeyboardInterrupt:
        print("Stopping stream.")
    finally:
        stream.stop_stream()
        stream.close()
        mic_stream.terminate()
