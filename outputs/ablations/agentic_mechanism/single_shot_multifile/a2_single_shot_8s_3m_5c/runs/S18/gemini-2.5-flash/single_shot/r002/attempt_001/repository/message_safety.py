import os
from typing import Dict, Any, List, Optional
import boto3

def get_boto3_client(service_name: str, region_name: Optional[str] = None):
    if region_name is None:
        region_name = os.environ.get("AWS_REGION", "us-east-1")
    return boto3.client(service_name, region_name=region_name)

def check_message_for_safety(
    message_text: str,
    language_code: str = "en",
    region_name: Optional[str] = None
) -> Dict[str, Any]:
    comprehend_client = get_boto3_client("comprehend", region_name=region_name)

    safety_report = {}

    try:
        sentiment_response = comprehend_client.detect_sentiment(
            Text=message_text,
            LanguageCode=language_code
        )
        safety_report['sentiment'] = {
            'Sentiment': sentiment_response['Sentiment'],
            'SentimentScore': sentiment_response['SentimentScore']
        }
    except Exception as e:
        safety_report['sentiment_error'] = str(e)

    try:
        pii_response = comprehend_client.detect_pii_entities(
            Text=message_text,
            LanguageCode=language_code
        )
        safety_report['pii_entities'] = pii_response['Entities']
        safety_report['has_pii'] = len(pii_response['Entities']) > 0
    except Exception as e:
        safety_report['pii_error'] = str(e)

    is_safe = True
    if 'sentiment' in safety_report and safety_report['sentiment']['Sentiment'] in ['NEGATIVE', 'MIXED'] and \
       safety_report['sentiment']['SentimentScore'].get('Negative', 0) > 0.7:
        is_safe = False
    if 'has_pii' in safety_report and safety_report['has_pii']:
        is_safe = False
    
    safety_report['is_safe_flag'] = is_safe

    return safety_report
