# Detect labels or objects in a static image using Clarifai
import os
import clarifai
from clarifai.rest import ClarifaiApp

# Local helper imports
from vision_client import get_clarifai_client
from vision_models import normalize_labels

app = get_clarifai_client()


def detect_image_labels(image_path: str):
    """Detect labels/objects in an image using Clarifai and return normalized labels."""
    client = app
    response = client.models.predict(
        model_id="aaa03c23b3724a16a56b629203edc62c",  # General model
        data={"inputs": [{"image": {"base64": clarifai.b64encode_file(image_path)}}]},
    )
    # Extract concepts (labels)
    labels = [concept["name"] for concept in response["outputs"][0]["data"]["concepts"]]
    return normalize_labels(labels)
