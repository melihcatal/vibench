import os
from google.cloud import videointelligence

def check_safety(text):
    client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.EXPLICIT_CONTENT_DETECTION]
    response = client.annotate_text(content=text, features=features)
    return response.explicit_annotation.categories[0].probability if response.explicit_annotation.categories else 0