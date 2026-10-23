from speech_client import get_polly_client
from speech_models import SynthesisResponse
from typing import Literal, NamedTuple

class SSMLSynthesisRequest(NamedTuple):
    ssml_text: str
    voice_id: str = "Joanna"  # AWS Polly default voice
    output_format: Literal["mp3", "ogg_vorbis", "pcm"] = "mp3"

def synthesize_ssml(request: SSMLSynthesisRequest) -> SynthesisResponse:
    """
    Synthesizes SSML with voice and prosody controls using AWS Polly.
    """
    polly_client = get_polly_client()
    response = polly_client.synthesize_speech(
        Text=request.ssml_text,
        OutputFormat=request.output_format,
        VoiceId=request.voice_id, # AWS provider-specific parameter
        TextType='ssml'
    )

    with response["AudioStream"] as stream:
        audio_bytes = stream.read()

    return SynthesisResponse(audio_stream=audio_bytes)
