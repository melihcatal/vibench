import os
from google.cloud import speech_v1p1beta1 as speech

def handle_streaming_recognition(response):
    if response.results:
        for result in response.results:
            if result.is_final:
                print(f"Final result: {result.alternatives[0].transcript}")
            else:
                print(f"Partial result: {result.alternatives[0].transcript}")

# Example usage
client = speech.SpeechClient()
config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="en-US",
)
streaming_config = speech.StreamingRecognitionConfig(config=config)

# Simulate streaming recognition response
response = speech.StreamingRecognizeResponse(
    results=[
        speech.StreamingRecognitionResult(
            is_final=False,
            alternatives=[speech.SpeechRecognitionAlternative(transcript="Hello")],
        ),
        speech.StreamingRecognitionResult(
            is_final=True,
            alternatives=[speech.SpeechRecognitionAlternative(transcript="Hello world!")],
        ),
    ]
)

handle_streaming_recognition(response)