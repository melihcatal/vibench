# message_safety.py
# [LATER-STEP]
# Scan Pub/Sub message payloads for unsafe or toxic content using Amazon Comprehend.

import os
import boto3
from .messaging_models import EventPayload

def scan_payload_for_unsafe(payload: EventPayload) -> bool:
    """Return True if the payload contains unsafe/toxic text according to Comprehend.

    This simple implementation checks the top‑level 'text' field of the payload.
    """
    text = payload.data.get('text', '')
    if not text:
        return False
    comprehend = boto3.client('comprehend', region_name='us-east-1')
    # Detect dominant language then sentiment; we use the toxicity API (Sentiment detection doesn't give toxicity,
    # but we can approximate with Sentiment and Entity detection. For demo purposes we treat 'NEGATIVE' sentiment as unsafe.)
    response = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    return response['Sentiment'] != 'POSITIVE'
