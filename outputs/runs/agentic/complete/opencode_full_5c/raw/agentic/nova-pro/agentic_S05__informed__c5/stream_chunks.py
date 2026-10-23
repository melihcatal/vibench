import os
from google.cloud import speech_v1 as speech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/credentials.json"

client = speech.SpeechClient()


def stream_chunks():
    print("Streaming audio chunks...")
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
            for content in recognize_from_async_source()
        )

        responses = client.streaming_recognize(streaming_config, requests)
        for response in responses:
            for result in response.results:
                print("Transcript: {}".format(result.alternatives[0].transcript))


def recognize_from_async_source():
    # Simulate async audio source
    import time

    while True:
        yield b"simulated_audio_chunk"
        time.sleep(1)


if __name__ == "__main__":
    stream_chunks()
