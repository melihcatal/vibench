from observability_client import ObservabilityClient
import os
from typing import List, Dict, Any


def check_log_text_safety(log_messages: List[str]) -> List[Dict[str, Any]]:
    client = ObservabilityClient()
    safety_results = []

    if not log_messages:
        return safety_results

    print(
        f"Checking {len(log_messages)} log messages for safety using Amazon Comprehend..."
    )

    for i, message in enumerate(log_messages):
        # Comprehend's detect_sentiment is used here as a proxy for content safety
        # A more direct content safety check would use services like Amazon Comprehend Toxicity Detection
        # or AWS Bedrock Guardrails, if available and configured for the specific type of safety required.
        # For this exercise, detect_sentiment will provide a basic analysis.
        try:
            response = client.detect_sentiment(message)
            safety_results.append(
                {
                    "original_message": message,
                    "sentiment": response["Sentiment"],
                    "sentiment_scores": response["SentimentScore"],
                }
            )
            print(f"  Message {i + 1} sentiment: {response['Sentiment']}")
        except Exception as e:
            safety_results.append({"original_message": message, "error": str(e)})
            print(f"  Error processing message {i + 1}: {e}")

    print("Log text safety check completed.")
    return safety_results


if __name__ == "__main__":
    # Example usage: Ensure AWS_REGION environment variable is set
    # Example: export AWS_REGION=us-east-1

    sample_log_messages = [
        "User 'johndoe' logged in successfully.",
        "Error: Failed to connect to critical service, system might be unstable!",
        "The application encountered an unexpected error and crashed.",
        "Warning: Potential unauthorized access attempt detected from IP 192.168.1.100.",
    ]

    results = check_log_text_safety(sample_log_messages)
    print("\n--- Log Safety Results ---")
    for res in results:
        print(json.dumps(res, indent=2))
