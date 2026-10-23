import os
from google.cloud import videointelligence

client = videointelligence.VideoIntelligenceServiceClient()

def check_safety(text):
    features = [videointelligence.Feature(model="TEXT_DETECTION")]
    operation = client.annotate_text(text=text, features=features)
    result = operation.result()
    return result.text_annotations[0].description
