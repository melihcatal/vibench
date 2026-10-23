from vision_client import load_config


def visual_safety_text(payload, config=None):
    cfg = load_config(config)
    labels = payload.get("labels", [])
    unsafe_terms = [item.get("name", "") for item in labels if item.get("confidence", 0.0) >= float(cfg.get("min_confidence", 0.5))]
    return {"unsafe_terms": unsafe_terms, "provider": "amazon-comprehend"}
