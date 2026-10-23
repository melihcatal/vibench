import os
import json
from typing import Dict, Any
from security_models import SafetyCheckResult
import boto3

def check_payload_safety(plaintext: str) -> SafetyCheckResult:
    """
    Check decrypted text payloads for unsafe content using Amazon Comprehend.
    """
    region = os.getenv('AWS_REGION', 'us-east-1')
    client = boto3.client('comprehend', region_name=region)
    
    try:
        # Detect toxic content using Amazon Comprehend
        response = client.detect_toxic_content(
            TextSegments=[{'Text': plaintext}],
            LanguageCode='en'
        )
        
        # Process results
        categories = {}
        for result in response['ResultList']]:
            for label in result['Labels']:
                categories[label['Name']] = label['Score']
        
        # Determine if content is safe (no toxic content above threshold)
        toxic_threshold = 0.5
        is_safe = all(score < toxic_threshold for score in categories.values())
        
        return SafetyCheckResult(
            is_safe=is_safe,
            categories=categories,
            provider='amazon_comprehend'
        )
        
    except Exception as e:
        return SafetyCheckResult(
            is_safe=False,
            categories={},
            provider='amazon_comprehend',
            error=str(e)
        )