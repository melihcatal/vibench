from vision_client import image_bytes, rekognition_client


def describe_image(source, max_labels=3):
    client = rekognition_client()
    response = client.detect_labels(Image={"Bytes": image_bytes(source)}, MaxLabels=max_labels, MinConfidence=60)
    labels = response.get("Labels", [])
    parts = [label.get("Name") for label in labels[:3] if label.get("Name")]
    if not parts:
        return ""
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + " and " + parts[-1]
