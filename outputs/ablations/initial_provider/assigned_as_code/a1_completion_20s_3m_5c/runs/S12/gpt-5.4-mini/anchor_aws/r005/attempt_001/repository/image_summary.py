from vision_client import load_config


def image_summary(payload, config=None):
    cfg = load_config(config)
    labels = payload.get("labels", [])
    text = payload.get("text", [])
    unsafe = payload.get("unsafe", [])
    summary = {
        "region": cfg.get("region"),
        "label_count": len(labels),
        "text_count": len(text),
        "unsafe_count": len(unsafe),
    }
    return summary
