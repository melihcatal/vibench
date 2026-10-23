from google.cloud import videointelligence

def live_caption_safety(text):
    client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.EXPLICIT_CONTENT_DETECTION]
    response = client.annotate_text(text, features=features)
    return response.explicit_annotation
