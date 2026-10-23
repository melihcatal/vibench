import os
import boto3
from typing import List, Dict, Any
from botocore.exceptions import ClientError
from security_models import AuditNote

class AWSComprehendClient:
    def __init__(self):
        self.client = boto3.client('comprehend')

    def detect_sentiment(self, text: str, language_code: str = 'en') -> Dict[str, Any]:
        try:
            response = self.client.detect_sentiment(Text=text, LanguageCode=language_code)
            return response
        except ClientError as e:
            print(f"Error detecting sentiment: {e}")
            raise

def check_secret_label_safety(audit_notes: List[AuditNote]) -> Dict[str, Any]:
    comprehend_client = AWSComprehendClient()
    safety_report = {}

    for note in audit_notes:
        unsafe_findings = []
        # Check content for unsafe text
        if note.content:
            sentiment_response = comprehend_client.detect_sentiment(note.content)
            if sentiment_response.get('Sentiment') in ['NEGATIVE', 'MIXED']:
                unsafe_findings.append({'type': 'content_sentiment', 'sentiment': sentiment_response.get('Sentiment')})

        # Check labels for unsafe text
        if note.labels:
            for key, value in note.labels.items():
                sentiment_response_key = comprehend_client.detect_sentiment(key)
                if sentiment_response_key.get('Sentiment') in ['NEGATIVE', 'MIXED']:
                    unsafe_findings.append({'type': 'label_key_sentiment', 'label_key': key, 'sentiment': sentiment_response_key.get('Sentiment')})

                sentiment_response_value = comprehend_client.detect_sentiment(value)
                if sentiment_response_value.get('Sentiment') in ['NEGATIVE', 'MIXED']:
                    unsafe_findings.append({'type': 'label_value_sentiment', 'label_value': value, 'sentiment': sentiment_response_value.get('Sentiment')})
        
        if unsafe_findings:
            safety_report[note.note_id] = unsafe_findings
    
    return safety_report
