import os
from clarifai.client.model import Model
from vision_client import load_image_bytes
from vision_models import ImageLabels

model = Model(
    model_id="aaa03c23b3724a16a56b629203edc62c", pat=os.getenv("CLARIFAI_PAT")
)


def detect_image_labels(image_path: str) -> ImageLabels:
    image_bytes = load_image_bytes(image_path)
    prediction = model.predict([image_bytes])
    concepts = prediction["outputs"][0]["data"]["concepts"][:10]
    labels = [concept["name"] for concept in concepts]
    confidence_scores = [concept["value"] for concept in concepts]
    return {"labels": labels, "confidence_scores": confidence_scores}
