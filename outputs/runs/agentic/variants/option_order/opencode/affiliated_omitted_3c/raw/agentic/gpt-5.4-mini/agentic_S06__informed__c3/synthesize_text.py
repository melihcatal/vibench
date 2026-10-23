from speech_client import create_polly_client, load_speech_config
from speech_models import SynthesisRequest, normalize_text


def synthesize_text(text: str, voice_id: str = None, output_format: str = None, language_code: str = None) -> bytes:
    cfg = load_speech_config()
    req = SynthesisRequest(
        text=normalize_text(text),
        voice_id=voice_id or cfg.voice_id,
        output_format=output_format or cfg.output_format,
        language_code=language_code or cfg.language_code,
    )
    client = create_polly_client()
    params = {
        "Text": req.text,
        "OutputFormat": req.output_format,
        "VoiceId": req.voice_id,
    }
    if req.language_code:
        params["LanguageCode"] = req.language_code
    resp = client.synthesize_speech(**params)
    return resp["AudioStream"].read()
