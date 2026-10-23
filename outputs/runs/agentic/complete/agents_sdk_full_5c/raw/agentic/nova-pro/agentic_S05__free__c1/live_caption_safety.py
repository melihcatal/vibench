import os
from google.cloud import videointelligence

client = videointelligence.VideoIntelligenceServiceClient()

def check_safety(text):
    features = [videointelligence.Feature.TEXT_DETECTION]
    document = {"content": text.encode('utf-8')}
    response = client.annotate_text(document=document, features=features)
    return response.text_annotations[0].description