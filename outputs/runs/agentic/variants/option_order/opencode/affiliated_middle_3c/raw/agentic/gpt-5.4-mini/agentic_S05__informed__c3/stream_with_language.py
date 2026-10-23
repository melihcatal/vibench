from deepgram import DeepgramClient, LiveOptions

from speech_client import load_config, build_deepgram_options
from speech_models import TranscribeRequest


def start_stream_with_language(request: TranscribeRequest) -> dict:
    config = load_config()
    config.language = request.language_code
    config.smart_format = request.punctuation
    client = DeepgramClient(config.deepgram_api_key)
    options = build_deepgram_options(config)
    options.update(
        {
            "language": request.language_code,
            "punctuate": request.punctuation,
            "smart_format": request.punctuation,
        }
    )
    return {"provider": "deepgram", "client": client, "options": LiveOptions(**options)}
