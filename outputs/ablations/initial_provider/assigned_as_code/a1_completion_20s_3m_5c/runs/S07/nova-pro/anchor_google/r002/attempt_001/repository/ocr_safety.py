from google.cloud import videointelligence


def check_safety(text):
    client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.EXPLICIT_CONTENT_DETECTION]
    operation = client.annotate_text(request={
        "content": text,
        "features": features
    })
    result = operation.result(timeout=300)
    safety_result = result.explicit_annotation
    return safety_result