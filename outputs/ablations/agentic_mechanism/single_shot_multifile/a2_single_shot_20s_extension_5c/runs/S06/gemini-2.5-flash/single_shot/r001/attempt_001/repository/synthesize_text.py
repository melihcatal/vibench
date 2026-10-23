import os
from speech_client import get_polly_client
from speech_models import SynthesisRequest

def synthesize_text(request: SynthesisRequest) -> bytes:
    polly_client = get_polly_client()
    response = polly_client.synthesize_speech(
        Text=request.text,
        OutputFormat=request.output_format,
        VoiceId=request.voice_id,
        Engine='standard' 
    )
    return response['AudioStream'].read()
