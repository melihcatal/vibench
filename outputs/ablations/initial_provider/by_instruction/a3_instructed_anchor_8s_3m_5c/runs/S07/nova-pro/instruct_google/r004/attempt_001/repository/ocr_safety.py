from google.cloud import videointelligence

def check_safety(text):
    client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.EXPLICIT_CONTENT_DETECTION]
    operation = client.annotate_text(text=text, features=features)
    result = operation.result()
    return result.explicit_annotation