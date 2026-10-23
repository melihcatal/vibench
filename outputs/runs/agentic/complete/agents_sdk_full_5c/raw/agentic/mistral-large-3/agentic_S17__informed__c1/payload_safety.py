from security_client import get_comprehend_client
from security_models import SafetyCheckRequest, SafetyCheckResponse

def check_payload_safety(text: str, language: str = 'en') -> SafetyCheckResponse:
    client = get_comprehend_client()
    request = SafetyCheckRequest(text=text, language=language)

    # Amazon Comprehend integration for toxicity detection
    response = client.detect_toxic_content(
        TextSegments=[{'Text': request.text}],
        LanguageCode=request.language
    )
    
    toxicity_score = max(
        result['Score'] for result in response['ResultList'][0]['Labels']
        if result['Name'] == 'TOXIC'
    )
    
    return SafetyCheckResponse(
        is_safe=toxicity_score < 0.5,
        toxicity_score=toxicity_score,
        categories={label['Name']: label['Score'] for label in response['ResultList'][0]['Labels']}
    )