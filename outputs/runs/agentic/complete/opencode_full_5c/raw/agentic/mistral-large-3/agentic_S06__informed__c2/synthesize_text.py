from typing import Optional
from speech_client import PollySpeechClient
from speech_models import SynthesisRequest


def synthesize_text(
    text: str, voice_id: str = "Joanna", output_format: str = "mp3"
) -> bytes:
    """
    Synthesizes plain text to an audio byte stream using Amazon Polly.
    """
    client = PollySpeechClient()
    request = SynthesisRequest(
        text=text, voice_id=voice_id, output_format=output_format, ssml=False
    )
    return client.synthesize(request.text, request.voice_id, request.output_format)
