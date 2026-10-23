from clarifai.client.input import Inputs
from vision_client import get_clarifai_app
from vision_models import ImageSafetyScore


def score_image_safety(image_bytes: bytes) -> list[ImageSafetyScore]:
    app = get_clarifai_app()
    model = app.models.get("moderation")

    image_input = Inputs.get_input_from_bytes(input_bytes=image_bytes)
    response = model.predict([image_input])

    outputs = response.outputs[0].data.concepts

    scores = [
        ImageSafetyScore(category=concept.name, probability=concept.value)
        for concept in outputs
    ]

    return scores
