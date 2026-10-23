from typing import Optional
from speech_client import PollySpeechClient
from speech_models import SynthesisRequest


def synthesize_ssml(
    ssml: str, voice_id: str = "Joanna", output_format: str = "mp3"
) -> bytes:
    """
    Synthesizes SSML with voice and prosody controls using Amazon Polly.
    """
    client = PollySpeechClient()
    request = SynthesisRequest(
        text=ssml, voice_id=voice_id, output_format=output_format, ssml=True
    )
    return client.synthesize(request.text, request.voice_id, request.output_format)
