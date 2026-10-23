import os
from clarifai.client.model import Model
from vision_client import b64_image


def detect_image_labels(image_path: str) -> dict:
    """
    Detects labels or objects in a static image using Clarifai.
    Returns: {'labels': [{'name': str, 'confidence': float}, ...]}
    """
    pat = os.getenv("CLARIFAI_PAT")
    if not pat:
        raise ValueError("Set CLARIFAI_PAT environment variable")

    model = Model(
        "aaa03c23b3724a16a56b629203edc62c",  # Clarifai Universal model
        user_id="clarifai",
        app_id="main",
        pat=pat,
    )

    image_b64 = b64_image(image_path)

    response = model.predict_base64(image_b64)

    labels = []
    for concept in response["data"]["concepts"][:10]:
        labels.append({"name": concept["name"], "confidence": float(concept["value"])})

    return {"labels": labels}
