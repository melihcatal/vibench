from vision_client import get_rekognition_client
from vision_models import normalize_labels

def describe_image(payload, config=None):
    config = config or {}
    client = get_rekognition_client(region_name=config.get("region"))

    labels_response = client.detect_labels(
        Image={"Bytes": payload["image_bytes"]},
        MaxLabels=int(config.get("max_labels", 10)),
    )
    labels = normalize_labels(labels_response)

    description_parts = []
    if labels:
        description_parts.append("The image contains: ")
        description_parts.append(", ".join([label["name"] for label in labels]))
    
    # Optionally add face detection for more detail, if faces are present.
    # However, for a *short visual description*, labels are often sufficient.
    # Keeping it simple for now, focusing on labels.
    
    return {"description": ". ".join(description_parts) + "."}
