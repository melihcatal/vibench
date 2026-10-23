from vision_client import VisionClient
from vision_models import VisualSafetyTextRequest, VisualSafetyTextResponse
import os

def visual_safety_text(request: VisualSafetyTextRequest) -> VisualSafetyTextResponse:
    client = VisionClient(region_name=os.environ.get('AWS_REGION', 'us-east-1')).comprehend_client
    response = client.detect_sentiment(
        Text=request.text,
        LanguageCode='en'  # Assuming English for sentiment analysis
    )
    sentiment = response.get('Sentiment')
    is_unsafe = False
    reasons = []

    if sentiment == 'NEGATIVE' or sentiment == 'MIXED':
        is_unsafe = True
        reasons.append(f"Text sentiment is {sentiment.lower()}.")
    
    # Add more sophisticated checks for specific keywords or patterns if needed

    return VisualSafetyTextResponse(is_unsafe=is_unsafe, reasons=reasons)
