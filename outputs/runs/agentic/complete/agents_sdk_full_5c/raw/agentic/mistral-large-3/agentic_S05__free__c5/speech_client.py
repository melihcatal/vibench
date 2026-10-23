from google.cloud import speech_v1p1beta1 as speech
import os

def get_speech_client():
    credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not credentials_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    return speech.SpeechClient()

async def streaming_recognize(client, config):
    return await client.streaming_recognize(config)