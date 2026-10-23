import os
import googleapiclient.discovery
from speech_models import TranscriptSegment
from typing import List, Dict, Any

def moderate_transcript_text(segments: List[TranscriptSegment]) -> List[Dict[str, Any]]:
    client = googleapiclient.discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=os.environ.get("PERSPECTIVE_API_KEY"),
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False
    )

    moderated_results = []
    for segment in segments:
        analyze_request = {
            'comment': {'text': segment.text},
            'requestedAttributes': {
                'TOXICITY': {},
                'SEVERE_TOXICITY': {},
                'IDENTITY_ATTACK': {},
                'INSULT': {},
                'PROFANITY': {},
                'THREAT': {},
            }
        }

        response = client.comments().analyze(body=analyze_request).execute()
        
        attribute_scores = {
            attribute: scores['summaryScore']['value']
            for attribute, scores in response['attributeScores'].items()
        }
        
        moderated_results.append({
            "segment_id": segment.id,
            "text": segment.text,
            "moderation_scores": attribute_scores
        })
    return moderated_results
