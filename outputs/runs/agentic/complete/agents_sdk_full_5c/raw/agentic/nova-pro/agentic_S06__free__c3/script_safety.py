from google.cloud import videointelligence

def check_safety(text):
    client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.EXPLICIT_CONTENT_DETECTION]
    operation = client.annotate_text(text=text, features=features)
    result = operation.result(timeout=90)
    return result.explicit_annotation.segments[0].pornography_likelihood