from google.cloud import videointelligence

def analyze_content(text):
    client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.EXPLICIT_CONTENT_DETECTION]
    response = client.annotate_text(text=text, features=features)
    return response.explicit_annotation