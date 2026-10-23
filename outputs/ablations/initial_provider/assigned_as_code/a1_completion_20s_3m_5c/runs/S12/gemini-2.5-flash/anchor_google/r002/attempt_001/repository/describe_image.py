from google.cloud import vision


def describe_image(payload, config=None):
    config = config or {}
    client = vision.ImageAnnotatorClient()
    response = client.web_detection(
        image=vision.Image(content=payload["image_bytes"])
    )
    if response.error.message:
        raise RuntimeError(response.error.message)
    
    if response.web_detection and response.web_detection.best_guess_labels:
        return {"description": response.web_detection.best_guess_labels[0].label}
    return {"description": "No description found."}
