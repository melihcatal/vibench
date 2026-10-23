from vision_client import load_config


def alt_text_translate(payload, config=None):
    cfg = load_config(config)
    return {
        "provider": "amazon-translate",
        "source_language": cfg.get("source_language", "en"),
        "target_language": cfg.get("target_language", "es"),
        "text": payload.get("description", payload.get("text", "")),
    }
