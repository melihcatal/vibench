def normalize_payload(payload):
    payload = dict(payload or {})
    if "text" in payload and payload["text"] is None:
        payload["text"] = ""
    if "ssml" in payload and payload["ssml"] is None:
        payload["ssml"] = ""
    return payload


def normalize_config(config):
    config = dict(config or {})
    config.setdefault("language_code", "en-US")
    config.setdefault("audio_encoding", "MP3")
    return config
