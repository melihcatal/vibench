import os
from google.cloud import videointelligence

client = videointelligence.VideoIntelligenceServiceClient()

def check_safety(text):
    features = [videointelligence.Feature.EXPLICIT_CONTENT_DETECTION]
    document = {"content": text.encode('utf-8')}
    response = client.annotate_text(document, features)
    return response.explicit_annotation.scenes[0].explicit_content_label