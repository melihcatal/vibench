import os
from google.cloud import speech_v1 as speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"

client = speech.SpeechClient()


def stream_microphone():
    print("Streaming microphone audio...")
    with speech.SpeechClient() as client:
        streaming_config = speech.StreamingRecognitionConfig(
            config=speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="en-US",
            ),
            interim_results=True,
        )

        audio_generator = recognize_from_microphone()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)
        for response in responses:
            for result in response.results:
                print("Transcript: {}".format(result.alternatives[0].transcript))


def recognize_from_microphone():
    import pyaudio

    p = pyaudio.PyAudio()
    stream = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024,
    )
    print("Start speaking...")
    while True:
        yield stream.read(1024)


if __name__ == "__main__":
    stream_microphone()
