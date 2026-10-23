import vision_client


def detect_image_text(payload, config=None):
    cfg = vision_client.get_provider_config(config)
    client = vision_client.rekognition_client(cfg["region"])
    response = client.detect_text(Image={"Bytes": payload["image_bytes"]})
    detections = []
    for item in response.get("TextDetections", []):
        if item.get("Type") == "LINE":
            detections.append({"text": item.get("DetectedText"), "confidence": item.get("Confidence", 0.0) / 100.0})
    return {"text": detections}
