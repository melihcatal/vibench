from google.cloud import videointelligence

def check_safety(text):
    client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.EXPLICIT_CONTENT_DETECTION]
    operation = client.annotate_text(text, features=features)
    result = operation.result(timeout=300)
    if result.explicit_annotation.frames[0].pornography_likelihood > videointelligence.Likelihood.POSSIBLE:
        return 'Unsafe'
    else:
        return 'Safe'