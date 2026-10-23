import os
from google.cloud import videointelligence

client = videointelligence.VideoIntelligenceServiceClient()

def check_safety(text):
    features = [videointelligence.Feature.TEXT_DETECTION]
    content = videointelligence.types.TextSegment(content=text)
    operation = client.annotate_text(features=features, text_segment=content)
    result = operation.result()
    return result.text_annotations[0].description if result.text_annotations else ''