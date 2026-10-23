import os
from google.cloud import speech_v1 as speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"

client = speech.SpeechClient()


def handle_partial_results():
    print("Handling partial and final streaming recognition events...")
    with speech.SpeechClient() as client:
        streaming_config = speech.StreamingRecognitionConfig(
            config=speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
                sample_rate_hertz=16000,
                language_code="en-US",
            ),
            interim_results=True,
        )

        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in recognize_from_microphone()
        )

        responses = client.streaming_recognize(streaming_config, requests)
        for response in responses:
            for result in response.results:
                if not result.is_final:
                    print(
                        "Partial transcript: {}".format(
                            result.alternatives[0].transcript
                        )
                    )
                else:
                    print(
                        "Final transcript: {}".format(result.alternatives[0].transcript)
                    )


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
    handle_partial_results()
