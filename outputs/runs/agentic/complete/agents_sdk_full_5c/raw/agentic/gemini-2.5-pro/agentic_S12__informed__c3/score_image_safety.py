
import os
from clarifai.client.model import Model
from vision_client import get_clarifai_client
from vision_models import SafetyScore

def score_image_safety(image_url: str) -> list[SafetyScore]:
    """
    Scores an image for safety using the Clarifai moderation model.
    """
    client = get_clarifai_client()
    
    # Using a specific Clarifai moderation model
    model = Model(
        user_id="clarifai",
        app_id="main",
        model_id="moderation-image-classification",
        pat=client.pat
    )
    
    prediction = model.predict_by_url(url=image_url, input_type="image")
    
    concepts = prediction.outputs[0].data.concepts
    
    return [
        SafetyScore(label=concept.name, score=concept.value)
        for concept in concepts
    ]
