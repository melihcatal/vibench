from speech_client import get_polly_client
from speech_models import SynthesisRequest, SynthesisResponse

def synthesize_text(request: SynthesisRequest) -> SynthesisResponse:
    """
    Synthesizes plain text to an audio byte stream using AWS Polly.
    """
    polly_client = get_polly_client()
    response = polly_client.synthesize_speech(
        Text=request.text,
        OutputFormat=request.output_format,
        VoiceId=request.voice_id # AWS provider-specific parameter
    )

    # The audio stream is a StreamingBody object, read its content
    with response["AudioStream"] as stream:
        audio_bytes = stream.read()

    return SynthesisResponse(audio_stream=audio_bytes)
