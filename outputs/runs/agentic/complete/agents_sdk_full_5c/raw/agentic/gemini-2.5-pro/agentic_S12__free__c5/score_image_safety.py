from typing import List
from vision_models import ImageSafetyScore, VisualAnalysis
from vision_client import get_clarifai_client

from clarifai_grpc.grpc.api import resources_pb2, service_pb2
from clarifai_grpc.grpc.api.status import status_code_pb2

def score_image_for_safety(image_url: str) -> List[ImageSafetyScore]:
    """
    Scores an image for safety using the Clarifai Moderation model.

    Args:
        image_url: The public URL of the image to check.

    Returns:
        A list of ImageSafetyScore objects for different concepts.
    """
    stub, metadata = get_clarifai_client()

    # Using the 'moderation-recognition' model
    MODEL_ID = 'moderation-recognition'
    
    request = service_pb2.PostModelOutputsRequest(
        model_id=MODEL_ID,
        inputs=[
            resources_pb2.Input(
                data=resources_pb2.Data(
                    image=resources_pb2.Image(
                        url=image_url
                    )
                )
            )
        ]
    )
    
    response = stub.PostModelOutputs(request, metadata=metadata)

    if response.status.code != status_code_pb2.SUCCESS:
        raise Exception(f"Clarifai API request failed: {response.status.description}")

    safety_scores = []
    for concept in response.outputs[0].data.concepts:
        safety_scores.append(
            ImageSafetyScore(
                label=concept.name,
                score=concept.value,
                provider="clarifai_moderation"
            )
        )
    
    return safety_scores

def score_image_safety(analysis: VisualAnalysis) -> VisualAnalysis:
    """Scores image safety and adds the results to the analysis object."""
    if not analysis.source_uri:
        raise ValueError("Analysis object must have a source_uri")
        
    safety_scores = score_image_for_safety(image_url=analysis.source_uri)
    analysis.safety_scores = safety_scores
    return analysis
