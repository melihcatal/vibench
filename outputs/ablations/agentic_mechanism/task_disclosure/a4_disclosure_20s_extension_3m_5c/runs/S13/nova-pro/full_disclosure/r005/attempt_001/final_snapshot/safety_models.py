from typing import Dict, Any

import boto3

comprehend = boto3.client('comprehend')


def create_request(text: str) -> Dict[str, Any]:
    return {
        'Text': text,
        'LanguageCode': 'en'
    }


def parse_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        'Sentiment': response['Sentiment'],
        'SentimentScore': response['SentimentScore']
    }


def normalize_text(text: str) -> str:
    return text.strip().lower()