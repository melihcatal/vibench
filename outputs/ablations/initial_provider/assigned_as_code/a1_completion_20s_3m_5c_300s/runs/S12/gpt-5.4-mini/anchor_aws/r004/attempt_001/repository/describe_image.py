import vision_client


def describe_image(payload, config=None):
    cfg = vision_client.get_provider_config(config)
    client = vision_client.rekognition_client(cfg["region"])
    response = client.detect_labels(Image={"Bytes": payload["image_bytes"]}, MaxLabels=cfg["max_labels"])
    labels = response.get("Labels", [])
    if not labels:
        return {"description": ""}
    names = [label["Name"] for label in labels[:3]]
    return {"description": ", ".join(names)}
