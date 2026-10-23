import os
import requests
import json

def redact_unsafe(text: str) -> dict:
    """
    Flags or redacts unsafe spans from text using Azure Content Moderator.
    """
    # Azure Content Moderator Text Moderation API endpoint
    endpoint = os.environ.get("AZURE_CONTENT_MODERATOR_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_MODERATOR_SUBSCRIPTION_KEY")

    if not endpoint or not key:
        raise ValueError("Azure Content Moderator endpoint and subscription key must be set in environment variables.")

    text_moderation_url = f"{endpoint}/contentmoderator/moderate/v1.0/ProcessText/fullnameresolution?classify=true"

    headers = {
        'Ocp-Apim-Subscription-Key': key,
        'Content-Type': 'text/plain'
    }

    try:
        response = requests.post(text_moderation_url, headers=headers, data=text.encode('utf-8'))
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)
        moderation_result = response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e), "message": "Failed to connect to Azure Content Moderator."}

    redacted_text = text
    unsafe_spans = []

    # Example of redacting terms flagged by Azure Content Moderator
    # Note: Azure Content Moderator itself doesn't directly redact, it flags terms.
    # Redaction logic needs to be implemented client-side based on the flagged terms.
    if 'Terms' in moderation_result:
        for term in moderation_result['Terms']:
            start_index = term['Index']
            end_index = start_index + len(term['Term'])
            unsafe_spans.append({
                "start": start_index,
                "end": end_index,
                "term": term['Term'],
                "category": term.get('Category', 'Unknown')
            })
            # Simple redaction: replace with asterisks
            redacted_text = redacted_text[:start_index] + '*' * len(term['Term']) + redacted_text[end_index:]

    return {
        "original_text": text,
        "redacted_text": redacted_text,
        "unsafe_spans": unsafe_spans,
        "raw_moderation_result": moderation_result
    }
