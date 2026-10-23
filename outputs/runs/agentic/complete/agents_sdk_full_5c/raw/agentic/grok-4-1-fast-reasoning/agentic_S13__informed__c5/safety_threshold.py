import os
import boto3
from typing import Dict, Any
from safety_client import DEFAULT_THRESHOLDS
from safety_models import normalize_safety_scores

def safety_threshold(text: str, custom_thresholds: Dict[str, float] = None) -> bool:
    session = boto3.Session(
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name='us-east-1'
    )
    comprehend = session.client('comprehend')
    resp = comprehend.detect_toxicity(Text=text, LanguageCode='en')
    toxicity = resp['Result']['Toxicity']
    scores = {'toxicity': toxicity}
    thresholds = custom_thresholds or DEFAULT_THRESHOLDS
    normalized = normalize_safety_scores(scores, thresholds)
    return normalized['overall_risk'] == 'safe'