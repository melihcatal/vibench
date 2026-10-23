import os
from typing import List, Dict, Any
from google.cloud import language_v1

# Google Cloud Natural Language API
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set

def summarize_audit_events(event_logs: List[Dict[str, Any]]) -> str:
    """Summarizes a list of audit event logs using Google Cloud Natural Language API."""
    client = language_v1.LanguageServiceClient()

    full_text_for_analysis = "\n".join([
        f"Event Type: {event.get('event_type', 'N/A')}, User: {event.get('user_id', 'N/A')}, "
        f"Provider: {event.get('provider', 'N/A')}, Details: {event.get('details', {})}"
        for event in event_logs
    ])

    if not full_text_for_analysis.strip():
        return "No audit events to summarize."

    document = language_v1.Document(
        content=full_text_for_analysis,
        type_=language_v1.Document.Type.PLAIN_TEXT,
        language="en" # Assuming English for now
    )

    # Using analyze_entities to get key entities, then synthesize a summary
    # A direct summarization API is not directly available in NL API, 
    # so we extract entities and sentiment to form a narrative summary.
    response = client.analyze_entities(document=document, encoding_type=language_v1.EncodingType.UTF8)

    summary_parts = []
    if response.entities:
        summary_parts.append("Key entities identified in audit events:")
        for entity in response.entities:
            summary_parts.append(f"- {entity.name} (Type: {language_v1.Entity.Type(entity.type_).name}, Salience: {entity.salience:.2f})")

    # Can also add sentiment analysis if desired
    # sentiment = client.analyze_sentiment(document=document).document_sentiment
    # summary_parts.append(f"\nOverall sentiment of events: Score={sentiment.score:.2f}, Magnitude={sentiment.magnitude:.2f}")

    if not summary_parts:
        return "Could not generate a detailed summary based on entities."

    return "\n".join(summary_parts)

if __name__ == "__main__":
    # Example audit events (from identity_models.py structure)
    from datetime import datetime
    example_events = [
        {
            "timestamp": datetime.now().isoformat(),
            "event_type": "LOGIN_SUCCESS",
            "user_id": "user_google_123",
            "provider": "Google",
            "details": {"ip": "192.168.1.1", "device": "Chrome on Mac"}
        },
        {
            "timestamp": datetime.now().isoformat(),
            "event_type": "LOGIN_FAILURE",
            "user_id": "user_okta_456",
            "provider": "Okta",
            "details": {"reason": "Invalid credentials", "ip": "203.0.113.4"}
        },
        {
            "timestamp": datetime.now().isoformat(),
            "event_type": "TOKEN_REFRESH",
            "user_id": "user_google_123",
            "provider": "Google",
            "details": {"new_expiry": "..."}
        },
    ]

    # Ensure GOOGLE_APPLICATION_CREDENTIALS points to a service account key file
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("WARNING: GOOGLE_APPLICATION_CREDENTIALS environment variable not set. "
              "Google Cloud Natural Language API calls may fail without authentication.")
        print("Please set it to the path of your service account key file.")
    
    print("\n--- Summarizing Audit Events ---")
    summary = summarize_audit_events(example_events)
    print(summary)

    print("\n--- Summarizing Empty Events ---")
    empty_summary = summarize_audit_events([])
    print(empty_summary)
