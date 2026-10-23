from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

# Define the streaming recognition request
def create_streaming_request(config, audio):
    return types.StreamingRecognizeRequest(
        config=config,
        audio_content=audio
    )