import os
from google.cloud import videointelligence

client = videointelligence.VideoIntelligenceServiceClient()

def check_safety(text):
    features = [videointelligence.Feature.TEXTUAL_TOXICITY_DETECTION]
    response = client.annotate_text(text=text, features=features)
    return response.text_annotations[0].toxicity_score