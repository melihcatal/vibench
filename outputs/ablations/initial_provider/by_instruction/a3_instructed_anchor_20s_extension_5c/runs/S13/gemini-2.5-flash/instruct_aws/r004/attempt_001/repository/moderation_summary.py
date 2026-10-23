import boto3
import os
from typing import Dict, Any, List

def summarize_moderation_decisions_aws(moderation_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Summarizes moderation decisions using AWS Comprehend for key phrase extraction.
    """
    comprehend = boto3.client(
        'comprehend',
        region_name=os.environ.get('AWS_REGION', 'us-east-1'),
        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
    )

    all_feedback_texts = []
    for result in moderation_results:
        if result.get('is_unsafe_based_on_sentiment'):
            all_feedback_texts.append(f"Content detected as {result.get('sentiment')}. Sentiment score: {result.get('sentiment_score')}.")
        
    combined_text = ". ".join(all_feedback_texts)
    
    if not combined_text:
        return {"summary": "No unsafe content detected across all messages.", "key_phrases": []}

    response = comprehend.detect_key_phrases(Text=combined_text, LanguageCode='en')
    
    key_phrases = [phrase['Text'] for phrase in response['KeyPhrases']]

    summary_text = f"Summary of moderation: {len(all_feedback_texts)} potentially unsafe items found. Key phrases: {', '.join(key_phrases)}."

    return {
        'summary': summary_text,
        'key_phrases': key_phrases,
        'provider': 'AWS Comprehend'
    }
