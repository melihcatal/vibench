import boto3
from typing import Dict, Any, List
from security_client import get_secrets_manager_client


def embed_audit_notes_for_semantic_search(secret_name: str) -> Dict[str, Any]:
    """Fetches secret audit notes (from description) and uses AWS Comprehend for sentiment analysis.

    Args:
        secret_name: The name of the secret to fetch audit notes from.

    Returns:
        A dictionary containing the secret name, audit notes (description), and sentiment analysis result.
    """
    secrets_client = get_secrets_manager_client()
    comprehend_client = boto3.client(
        "comprehend", region_name="us-east-1"
    )  # Specify a region for Comprehend

    try:
        response = secrets_client.describe_secret(SecretId=secret_name)
        audit_notes = response.get("Description", "No audit notes found.")

        if audit_notes and audit_notes != "No audit notes found.":
            sentiment_response = comprehend_client.detect_sentiment(
                Text=audit_notes,
                LanguageCode="en",  # Assuming English for audit notes
            )
            sentiment_result = sentiment_response.get("Sentiment")
            sentiment_scores = sentiment_response.get("SentimentScore")
        else:
            sentiment_result = "N/A"
            sentiment_scores = {}

        return {
            "secret_name": secret_name,
            "audit_notes": audit_notes,
            "sentiment_analysis": {
                "sentiment": sentiment_result,
                "scores": sentiment_scores,
            },
        }

    except secrets_client.exceptions.ResourceNotFoundException:
        raise ValueError(f"Secret '{secret_name}' not found.")
    except Exception as e:
        raise RuntimeError(f"Error processing audit notes for semantic search: {e}")
