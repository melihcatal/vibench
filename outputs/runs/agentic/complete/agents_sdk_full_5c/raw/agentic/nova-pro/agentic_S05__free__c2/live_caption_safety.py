from google.cloud import videointelligence_v1 as videointelligence

def check_caption_safety(text):
    client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.EXPLICIT_CONTENT_DETECTION]
    response = client.annotate_text(text, features=features)
    return response.explicit_annotation.segments