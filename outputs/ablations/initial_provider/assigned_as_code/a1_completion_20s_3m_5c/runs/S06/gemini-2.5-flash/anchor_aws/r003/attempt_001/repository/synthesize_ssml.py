from speech_client import get_polly_client
from speech_models import SynthesizeSsmlInput, AudioOutput

def synthesize_ssml(payload: SynthesizeSsmlInput) -> AudioOutput:
    client = get_polly_client()
    response = client.synthesize_speech(
        Text=payload.ssml,
        TextType="ssml",
        OutputFormat=payload.output_format,
        VoiceId=payload.voice_id
    )
    stream = response["AudioStream"]
    try:
        return AudioOutput(audio_bytes=stream.read(), content_type=f"audio/{payload.output_format}")
    finally:
        stream.close()
