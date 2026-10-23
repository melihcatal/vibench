import os
import boto3
import json
from typing import List, Dict, Any

# AWS Comprehend for text analysis of audit logs
# AWS credentials will be picked up from environment variables or ~/.aws/credentials
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")

comprehend_client = boto3.client("comprehend", region_name=AWS_REGION)

def analyze_audit_notes(text_list: List[str]) -> List[Dict[str, Any]]:
    """Analyzes a list of audit event notes using AWS Comprehend for sentiment and key phrases."""
    if not text_list:
        return []

    results = []
    for text in text_list:
        try:
            sentiment_response = comprehend_client.detect_sentiment(Text=text, LanguageCode="en")
            key_phrases_response = comprehend_client.detect_key_phrases(Text=text, LanguageCode="en")
            
            results.append({
                "original_text": text,
                "sentiment": sentiment_response["Sentiment"],
                "sentiment_scores": sentiment_response["SentimentScore"],
                "key_phrases": [kp["Text"] for kp in key_phrases_response["KeyPhrases"]],
            })
        except Exception as e:
            print(f"Error analyzing text with AWS Comprehend: {e}")
            results.append({"original_text": text, "error": str(e)})
    return results

def summarize_audit_events(audit_events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Summarizes a list of audit events, including sentiment and key phrase analysis of notes."""
    summary = {
        "total_events": len(audit_events),
        "events_by_type": {},
        "events_by_provider": {},
        "sentiment_analysis": [],
        "common_key_phrases": {}
    }

    all_notes_text = []

    for event in audit_events:
        event_type = event.get("event_type", "unknown")
        provider = event.get("provider", "unknown")
        notes = event.get("notes")

        summary["events_by_type"][event_type] = summary["events_by_type"].get(event_type, 0) + 1
        summary["events_by_provider"][provider] = summary["events_by_provider"].get(provider, 0) + 1

        if notes:
            all_notes_text.append(notes)
    
    if all_notes_text:
        sentiment_results = analyze_audit_notes(all_notes_text)
        summary["sentiment_analysis"] = sentiment_results

        # Aggregate key phrases
        key_phrase_counts = {}
        for res in sentiment_results:
            for phrase in res.get("key_phrases", []):
                key_phrase_counts[phrase] = key_phrase_counts.get(phrase, 0) + 1
        summary["common_key_phrases"] = dict(sorted(key_phrase_counts.items(), key=lambda item: item[1], reverse=True))

    return summary

if __name__ == "__main__":
    # Example audit events (e.g., loaded from a database or log file)
    example_audit_events = [
        {
            "timestamp": "2023-10-26T10:00:00",
            "user_id": "user-1",
            "provider": "google",
            "event_type": "login_success",
            "notes": "User logged in successfully from a new device. Multi-factor authentication was used."
        },
        {
            "timestamp": "2023-10-26T10:05:00",
            "user_id": "user-2",
            "provider": "okta",
            "event_type": "login_failure",
            "notes": "Attempted login with incorrect password. Account locked for 5 minutes."
        },
        {
            "timestamp": "2023-10-26T10:10:00",
            "user_id": "user-1",
            "provider": "google",
            "event_type": "token_refresh",
            "notes": "Access token refreshed automatically."
        },
        {
            "timestamp": "2023-10-26T10:15:00",
            "user_id": "user-3",
            "provider": "okta",
            "event_type": "login_success",
            "notes": "Successful login from a known location. No suspicious activity detected."
        },
        {
            "timestamp": "2023-10-26T10:20:00",
            "user_id": "user-2",
            "provider": "okta",
            "event_type": "login_failure",
            "notes": "Further failed login attempts. IP address flagged as suspicious."
        },
    ]

    print("Summarizing example audit events...")
    audit_summary = summarize_audit_events(example_audit_events)
    print(json.dumps(audit_summary, indent=2))
