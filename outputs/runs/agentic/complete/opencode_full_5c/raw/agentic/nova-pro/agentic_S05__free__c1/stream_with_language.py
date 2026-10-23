import os
from google.cloud import speech_v1p1beta1 as speech


def stream_with_language(language_code="en-US"):
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config)

    client = speech.SpeechClient()

    with speech.MicrophoneStream(rate=16000) as stream:
        audio_generator = stream.generator()
        requests = (
            speech.StreamingRecognizeRequest(audio_content=content)
            for content in audio_generator
        )

        responses = client.streaming_recognize(streaming_config, requests)

        for response in responses:
            for result in response.results:
                print(result.alternatives[0].transcript)
