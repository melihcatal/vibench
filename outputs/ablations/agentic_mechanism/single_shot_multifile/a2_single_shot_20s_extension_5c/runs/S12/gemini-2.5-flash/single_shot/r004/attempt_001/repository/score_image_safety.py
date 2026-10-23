import os
import base64
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from vision_models import ImageInput, SafetyScoreResult

def score_image_safety(image_input: ImageInput) -> SafetyScoreResult:
    endpoint = os.environ.get('AZURE_AI_VISION_ENDPOINT')
    key = os.environ.get('AZURE_AI_VISION_KEY')

    if not endpoint or not key:
        raise ValueError("Azure AI Vision endpoint and key must be set as environment variables.")

    client = ImageAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

    features = [
        VisualFeatures.ADULT
    ]

    if image_input.content_base64:
        image_data = base64.b64decode(image_input.content_base64)
        result = client.analyze(image_data=image_data, visual_features=features)
    elif image_input.image_uri:
        result = client.analyze(image_url=image_input.image_uri, visual_features=features)
    else:
        raise ValueError("ImageInput must contain either content_base64 or image_uri")

    safety_scores = {}
    if result.adult:
        safety_scores['adult'] = {'is_adult_content': result.adult.is_adult_content, 'adult_score': result.adult.adult_score}
        safety_scores['racy'] = {'is_racy_content': result.adult.is_racy_content, 'racy_score': result.adult.racy_score}
        safety_scores['gore'] = {'is_gory_content': result.adult.is_gory_content, 'gore_score': result.adult.gore_score}
    
    return SafetyScoreResult(safety_scores=safety_scores)