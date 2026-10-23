import os
from google.cloud import videointelligence

def check_safety(text):
    client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.TEXT_DETECTION]
    operation = client.annotate_text(text, features=features)
    result = operation.result(timeout=90)
    return any(annotation.description == 'HARMFUL' for annotation in result.text_annotations)
