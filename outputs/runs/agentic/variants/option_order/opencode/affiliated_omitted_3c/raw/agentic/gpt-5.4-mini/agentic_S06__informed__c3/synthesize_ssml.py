from speech_client import create_polly_client, load_speech_config
from speech_models import SynthesisRequest


def synthesize_ssml(ssml: str, voice_id: str = None, output_format: str = None) -> bytes:
    cfg = load_speech_config()
    req = SynthesisRequest(text=ssml, voice_id=voice_id or cfg.voice_id, output_format=output_format or cfg.output_format)
    client = create_polly_client()
    resp = client.synthesize_speech(Text=req.text, TextType="ssml", OutputFormat=req.output_format, VoiceId=req.voice_id)
    return resp["AudioStream"].read()
