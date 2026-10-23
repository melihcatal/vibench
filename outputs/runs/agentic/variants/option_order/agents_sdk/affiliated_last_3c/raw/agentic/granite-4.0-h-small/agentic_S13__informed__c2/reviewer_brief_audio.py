import os
from aws_sdk_example import comprehend_client
from safety_models import ModSafetyResponse
import json

def reviewer_brief_audio(text: str) -> ModSafetyResponse:
    """Generate a spoken (audio) brief for moderation reviewers.
    This example calls Amazon Polly TTS via boto3 as a concrete provider.
    It returns the raw response (audio stream URL, SSML, etc.).
    """
    # Assume comprehend_client is a boto3 client configured elsewhere in aws_sdk_example
    client = comprehend_client
    # Create SSML markup from moderation summary
    summary = comprehend_client.detect_sentiment(Text=text, LanguageCode='en')
    ssml = f"<speak><prosody rate='medium'>{summary.get('sentiment','neutral')}</prosody></speak>"
    # Call Polly to synthesize speech
    resp = client.start_speech_synthesis_task(Text=ssml,
                                              TextType='ssml',
                                              OutputFormat='mp3',
                                              VoiceId='Matthew')
    return {'provider': 'AWS Polly', 'raw_response': resp}

__all__ = ['reviewer_brief_audio']
