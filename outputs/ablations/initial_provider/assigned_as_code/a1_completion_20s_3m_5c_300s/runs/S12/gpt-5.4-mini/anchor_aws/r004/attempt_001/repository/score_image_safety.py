import vision_client


def score_image_safety(payload, config=None):
    cfg = vision_client.get_provider_config(config)
    client = vision_client.rekognition_client(cfg["region"])
    response = client.detect_moderation_labels(Image={"Bytes": payload["image_bytes"]})
    labels = [{"name": label["Name"], "confidence": label["Confidence"] / 100.0} for label in response.get("ModerationLabels", [])]
    return {"unsafe": any(item["confidence"] >= 0.5 for item in labels), "labels": labels}
