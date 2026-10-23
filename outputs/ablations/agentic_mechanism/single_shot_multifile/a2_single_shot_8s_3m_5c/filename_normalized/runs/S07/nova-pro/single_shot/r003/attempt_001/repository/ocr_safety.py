import os
from google.cloud import videointelligence

def check_safety(text):
    client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.TEXT_DETECTION]
    response = client.annotate_text(text=text, features=features)
    return response.text_annotations[0].description if response.text_annotations else None