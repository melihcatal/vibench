import requests
import os
from vision_client import load_image_bytes
from vision_models import ImageSafety

def score_image_safety(image_path: str) -> ImageSafety:
    endpoint = os.getenv('AZURE_CONTENT_MODERATOR_ENDPOINT')
    key = os.getenv('AZURE_CONTENT_MODERATOR_KEY')
    url = f"{endpoint.rstrip('/')}/contentmoderator/moderate/v1.0/ProcessImage/Evaluate"
    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'image/jpeg',
    }
    image_bytes = load_image_bytes(image_path)
    response = requests.post(url, headers=headers, data=image_bytes)
    response.raise_for_status()
    data = response.json()
    adult_score = data.get('ImageAdultClassification', {}).get('AdultScore')
    racy_score = data.get('ImageRacyClassification', {}).get('RacyScore')
    gore_score = data.get('ImageGoryClassification', {}).get('GoryScore')
    return ImageSafety(
        adult_score=adult_score,
        racy_score=racy_score,
        gore_score=gore_score
    )