import os
from googleapiclient import discovery

def moderate_batch(texts: list[str]) -> list[dict]:
    """
    Moderates a batch of user messages and returns per-message decisions using Google Cloud Perspective API.
    """
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=os.environ.get('PERSPECTIVE_API_KEY')
    )

    results = []
    for text in texts:
        analyze_request = {
            'comment': {'text': text},
            'requestedAttributes': {
                'TOXICITY': {},
                'SEVERE_TOXICITY': {},
                'IDENTITY_ATTACK': {},
                'INSULT': {},
                'PROFANITY': {},
                'THREAT': {}
            }
        }

        response = client.comments().analyze(body=analyze_request).execute()
        
        # Process the response to fit a generic moderation decision format
        moderation_decision = {
            "text": text,
            "is_unsafe": False,
            "scores": {},
            "raw_perspective_response": response
        }

        if 'attributeScores' in response:
            for attribute, scores in response['attributeScores'].items():
                if 'summaryScore' in scores:
                    score_value = scores['summaryScore']['value']
                    moderation_decision["scores"][attribute.lower()] = score_value
                    if score_value > 0.7:  # Example threshold for marking as unsafe
                        moderation_decision["is_unsafe"] = True

        results.append(moderation_decision)

    return results
