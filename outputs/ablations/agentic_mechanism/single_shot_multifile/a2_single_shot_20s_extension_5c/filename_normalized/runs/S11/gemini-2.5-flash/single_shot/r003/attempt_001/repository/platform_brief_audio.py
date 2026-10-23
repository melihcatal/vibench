import os
from model_client import get_polly_client

def generate_speech_from_text(text: str, voice_id: str = "Joanna", output_format: str = "mp3") -> bytes:
    polly_client = get_polly_client()
    
    response = polly_client.synthesize_speech(
        Text=text,
        OutputFormat=output_format,
        VoiceId=voice_id,
        Engine="standard"
    )
    
    if "AudioStream" in response:
        with response["AudioStream"] as stream:
            return stream.read()
    else:
        raise RuntimeError("Could not get audio stream from AWS Polly.")
