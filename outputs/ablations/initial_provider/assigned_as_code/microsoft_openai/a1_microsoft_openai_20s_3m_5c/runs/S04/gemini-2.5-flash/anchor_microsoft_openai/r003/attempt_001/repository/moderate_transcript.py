import os
from google.cloud import language_v1
from typing import List
from speech_models import TranscriptSegment

def moderate_transcript(segments: List[TranscriptSegment], project_id: str) -> List[Dict[str, Any]]:
    client = language_v1.LanguageServiceClient()
    
    moderation_results = []
    for i, segment in enumerate(segments):
        document = language_v1.Document(
            content=segment.text,
            type_=language_v1.Document.Type.PLAIN_TEXT,
            language="en" # Assuming English for moderation
        )
        
        # Perform content classification to identify potentially problematic content
        # Note: Google Cloud Natural Language API's primary function is sentiment, entity, syntax analysis.
        # For explicit content moderation, other services like Google Cloud Video Intelligence API (for video content) or custom solutions might be more suitable.
        # However, for text-based content, we can use content classification as a form of moderation.
        response = client.classify_text(request={'document': document})
        
        categories = []
        for category in response.categories:
            categories.append({'name': category.name, 'confidence': category.confidence})
        
        moderation_results.append({
            "segment_index": i,
            "text": segment.text,
            "categories": categories,
            "contains_sensitive_content": any(cat['confidence'] > 0.7 for cat in categories if "/Adult" in cat['name'] or "/Violence" in cat['name'])
        })

    return moderation_results
