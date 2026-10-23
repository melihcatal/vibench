import os
from speech_client import get_polly_client
from speech_models import SSMLSynthesisRequest

def synthesize_ssml(request: SSMLSynthesisRequest) -> bytes:
    polly_client = get_polly_client()
    response = polly_client.synthesize_speech(
        Text=request.ssml_text,
        OutputFormat=request.output_format,
        VoiceId=request.voice_id,
        TextType='ssml',
        Engine='neural'
    )
    return response['AudioStream'].read()
