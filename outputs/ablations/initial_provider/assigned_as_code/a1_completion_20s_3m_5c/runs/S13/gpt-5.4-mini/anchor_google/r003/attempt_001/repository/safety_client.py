import os


def get_openai_api_key(config=None):
    config = config or {}
    return config.get("api_key") or os.environ["OPENAI_API_KEY"]


def get_openai_base_url(config=None):
    config = config or {}
    return config.get("base_url") or os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")


def get_openai_headers(config=None):
    return {
        "Authorization": f"Bearer {get_openai_api_key(config)}",
        "Content-Type": "application/json",
    }


def get_model(config=None, default="gpt-5.4-mini"):
    config = config or {}
    return config.get("model") or os.environ.get("OPENAI_MODEL", default)


def get_tts_voice(config=None, default="alloy"):
    config = config or {}
    return config.get("voice") or os.environ.get("OPENAI_TTS_VOICE", default)
