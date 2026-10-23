from googleapiclient.errors import HttpError
from security_client import perspective_client
from security_models import SafetyCheckRequest, SafetyCheckResponse

def check_payload_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    """
    Checks decrypted text for toxicity and other attributes using Perspective API.
    """
    try:
        client = perspective_client.get_client()
        
        analyze_request = {
            'comment': {'text': request.text},
            'requestedAttributes': {
                'TOXICITY': {},
                'SEVERE_TOXICITY': {},
                'IDENTITY_ATTACK': {},
                'INSULT': {},
                'PROFANITY': {},
                'THREAT': {}
            },
            'languages': ['en']
        }
        
        response = client.comments().analyze(body=analyze_request).execute()
        
        scores = {}
        is_safe = True
        for attr, data in response['attributeScores'].items():
            score = data['summaryScore']['value']
            scores[attr] = score
            if score > 0.7:
                is_safe = False

        return SafetyCheckResponse(
            is_safe=is_safe,
            scores=scores,
            success=True
        )
    except HttpError as e:
        return SafetyCheckResponse(
            is_safe=False,
            scores={},
            success=False,
            error=str(e)
        )
