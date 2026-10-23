import os
import boto3
from vision_client import image_to_bytes
from vision_models import ImageSafety

def score_image_safety(image_path: str) -> ImageSafety:
    rekognition = boto3.client('rekognition')
    img_bytes = image_to_bytes(image_path)
    response = rekognition.detect_moderation_labels(Image={'Bytes': img_bytes}, MinConfidence=60)
    risks = []
    scores = {}
    for label in response['ModerationLabels']:
        name = label['Name']
        conf = label['Confidence']
        scores[name] = conf
        if conf >= 60:
            risks.append(name)
    is_safe = len(risks) == 0
    return {'is_safe': is_safe, 'risks': risks, 'scores': scores}