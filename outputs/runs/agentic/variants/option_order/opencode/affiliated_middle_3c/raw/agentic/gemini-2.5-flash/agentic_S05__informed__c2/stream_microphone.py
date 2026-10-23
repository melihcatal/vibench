import pyaudio
from google.cloud import speech
from speech_client import get_speech_client
from speech_models import SpeechConfig

# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


def stream_microphone_audio():
    client = get_speech_client()
    config = SpeechConfig()

    audio_config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=RATE,
        language_code=config.language_code,
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

    print("Listening... Press Ctrl+C to stop.")
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
