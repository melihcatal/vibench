import os
from google.cloud import videointelligence

def moderate_transcript(transcript):
    client = videointelligence.VideoIntelligenceServiceClient()
    response = client.annotate_text({
        'document': {
            'content': transcript,
            'type_': videointelligence.Document.Type.PLAIN_TEXT,
        },
        'features': [videointelligence.Feature.TEXTUAL_MODERATION],
    })
    return response.textual_moderation_annotation