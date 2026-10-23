import os
from speech_client import TextToSpeechClient  # Azure provider

def synthesize(text: str, output_path: str):
    client = TextToSpeechClient()
    response = client.synthesize_speech(
        text=text,
        voice_name=client.default_voice,
        format='riff-16khz-16bit-mono-pcm'
    )
    with open(output_path, 'wb') as f:
        f.write(response.audio_data)
