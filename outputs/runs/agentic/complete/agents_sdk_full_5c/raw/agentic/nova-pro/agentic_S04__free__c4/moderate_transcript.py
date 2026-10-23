from google.cloud import videointelligence_v1 as videointelligence

def moderate_transcript(transcript):
    client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.Feature.EXPLICIT_CONTENT_DETECTION]
    operation = client.annotate_text(content=transcript, features=features)
    result = operation.result(timeout=90)
    return result.segment_label_annotations