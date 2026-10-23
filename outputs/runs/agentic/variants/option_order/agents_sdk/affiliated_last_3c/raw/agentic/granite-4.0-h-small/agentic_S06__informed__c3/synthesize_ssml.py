import os
from speech_client import TextToSpeechClient  # Azure provider

def synthesize_ssml(ssml: str, output_path: str):
    client = TextToSpeechClient()
    response = client.synthesize_speech(
        text=ssml,
        voice_name=client.default_voice,
        ssml=True,
        format='riff-16khz-16bit-mono-pcm'
    )
    with open(output_path, 'wb') as f:
        f.write(response.audio_data)
