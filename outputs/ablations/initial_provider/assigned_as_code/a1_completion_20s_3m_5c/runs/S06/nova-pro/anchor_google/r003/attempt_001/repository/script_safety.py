from google.cloud import videointelligence

def check_safety(script):
    client = videointelligence.VideoIntelligenceServiceClient()
    response = client.annotate_text(request={
        'parent': 'projects/YOUR_PROJECT_ID/locations/global',
        'text': script,
        'features': [videointelligence.TextAnnotationFeatures.SAFE_SEARCH]
    })
    return response.text_annotations[0].safe_search_annotation
