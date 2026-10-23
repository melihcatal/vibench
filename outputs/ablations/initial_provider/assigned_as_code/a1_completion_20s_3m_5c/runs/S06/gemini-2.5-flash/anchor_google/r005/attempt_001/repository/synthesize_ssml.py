from speech_client import TextToSpeechClient
from speech_models import SynthesisRequest, SynthesisResponse

def synthesize_ssml(payload, config=None) -> SynthesisResponse:
    config = config or {}
    client = TextToSpeechClient()
    request = SynthesisRequest(
        ssml=payload["ssml"],
        language_code=config.get("language_code", "en-US"),
        voice_name=config.get("voice_name"),
        audio_encoding=config.get("audio_encoding", "MP3")
    )
    return client.synthesize(request)
