import os


def load_speech_config(config=None):
    config = dict(config or {})
    config.setdefault("api_key", os.environ.get("AZURE_SPEECH_KEY"))
    config.setdefault("region", os.environ.get("AZURE_SPEECH_REGION", "eastus"))
    config.setdefault("language_code", os.environ.get("AZURE_SPEECH_LANGUAGE", "en-US"))
    config.setdefault("sample_rate_hz", int(os.environ.get("AZURE_SPEECH_SAMPLE_RATE", "16000")))
    config.setdefault("punctuation", True)
    config.setdefault("translation_target_language", os.environ.get("AZURE_TRANSLATION_TARGET_LANGUAGE", "es"))
    config.setdefault("safety_endpoint", os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT"))
    config.setdefault("embedding_model", os.environ.get("AZURE_EMBEDDING_MODEL", "text-embedding-3-small"))
    config.setdefault("summary_model", os.environ.get("AZURE_SUMMARY_MODEL", "gpt-4o-mini"))
    return config


def speech_client_config(config=None):
    return load_speech_config(config)
