# [SAME-SCENARIO] partial_results.py
# Handles partial and final streaming recognition events using Google Cloud Speech-to-Text
import json
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import enums
from google.cloud.speech_v1p1beta1.types import RecognitionConfig

# Google Cloud authentication
GOOGLE_APPLICATION_CREDENTIALS = "${GOOGLE_APPLICATION_CREDENTIALS}"

# Configurations
sample_rate_hertz = 16000
time_constant = 0.5  # seconds

recognizer_client = speech.SpeechClient()
config = RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=sample_rate_hertz,
    language_code="en-US",
    interim_results=True,
)

partial_context = []


def handle_event(event):
    if event.type == enums.StreamingRecognizeResultType.RESULT:
        if event.result.is_final:
            print("Final transcript:", event.result.alternatives[0].transcript)
        else:
            partial = event.result.alternatives[0].transcript
            partial_context.append(partial)
            print("Partial transcript:", partial)
    # Could add finalization logic or context handling here


async def stream_with_google_audio(audio_generator):
    request = speech.StreamingRecognizeRequest(audio_config=config)
    responses = recognizer_client.streaming_recognize(config, audio_generator)

    async for response in responses:
        for result in response.results:
            handle_event(result)


if __name__ == "__main__":
    # Placeholder for async audio generator
    stream_with_google_audio(asyncio.sleep(10))
