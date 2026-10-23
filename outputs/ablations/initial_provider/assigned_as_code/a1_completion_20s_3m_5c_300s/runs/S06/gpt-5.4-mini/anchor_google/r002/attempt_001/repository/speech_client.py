from google.cloud import texttospeech


def load_tts_config(config=None):
    config = config or {}
    return {
        "language_code": config.get("language_code", "en-US"),
        "voice_name": config.get("voice_name"),
        "ssml_gender": config.get("ssml_gender"),
        "audio_encoding": config.get("audio_encoding", texttospeech.AudioEncoding.MP3),
        "speaking_rate": config.get("speaking_rate"),
        "pitch": config.get("pitch"),
        "sample_rate_hertz": config.get("sample_rate_hertz"),
    }


def get_tts_client():
    return texttospeech.TextToSpeechClient()


def build_voice_params(config):
    params = {"language_code": config["language_code"]}
    if config.get("voice_name"):
        params["name"] = config["voice_name"]
    if config.get("ssml_gender") is not None:
        params["ssml_gender"] = config["ssml_gender"]
    return texttospeech.VoiceSelectionParams(**params)


def build_audio_config(config):
    params = {"audio_encoding": config["audio_encoding"]}
    for key in ("speaking_rate", "pitch", "sample_rate_hertz"):
        if config.get(key) is not None:
            params[key] = config[key]
    return texttospeech.AudioConfig(**params)
