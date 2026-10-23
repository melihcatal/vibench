import json
import os
from typing import List, Dict, Any

import boto3

from messaging_models import Message

def summarize_messages(messages: List[Message], region_name: str) -> Dict[str, Any]:
    """
    Analyzes the sentiment of message payloads using AWS Comprehend
    and provides a summary of messages processed.
    """
    comprehend_client = boto3.client("comprehend", region_name=region_name)

    summary_results = {
        "total_messages": len(messages),
        "sentiment_analysis": [],
        "processing_status": "completed"
    }

    for message in messages:
        # Assuming the message body contains a 'text' field for sentiment analysis
        message_text = message.body.get("text")
        if message_text and isinstance(message_text, str):
            try:
                sentiment_response = comprehend_client.detect_sentiment(Text=message_text, LanguageCode='en') # Assuming 'en'
                summary_results["sentiment_analysis"].append({
                    "message_id": message.id,
                    "sentiment": sentiment_response["Sentiment"],
                    "sentiment_scores": sentiment_response["SentimentScore"]
                })
            except Exception as e:
                summary_results["sentiment_analysis"].append({
                    "message_id": message.id,
                    "error": str(e)
                })
        else:
            summary_results["sentiment_analysis"].append({
                "message_id": message.id,
                "note": "No text content found for sentiment analysis"
            })

    return summary_results
