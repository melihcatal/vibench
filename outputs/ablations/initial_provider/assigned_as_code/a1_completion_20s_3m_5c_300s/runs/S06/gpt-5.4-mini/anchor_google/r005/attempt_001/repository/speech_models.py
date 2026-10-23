from google.cloud import texttospeech


def normalize_text_payload(payload):
    return {"text": payload.get("text", "")}


def normalize_ssml_payload(payload):
    return {"ssml": payload.get("ssml", "")}


def voice_params_from_config(config):
    return texttospeech.VoiceSelectionParams(
        language_code=config.get("language_code", "en-US"),
        name=config.get("voice_name"),
        ssml_gender=getattr(texttospeech.SsmlVoiceGender, config.get("ssml_gender", "NEUTRAL")),
    )


def audio_config_from_config(config):
    return texttospeech.AudioConfig(
        audio_encoding=config.get("audio_encoding", texttospeech.AudioEncoding.MP3),
        speaking_rate=config.get("speaking_rate", 1.0),
        pitch=config.get("pitch", 0.0),
    )
