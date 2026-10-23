from observability_client import ObservabilityClient
import os
from typing import List, Dict, Any
import json


def summarize_incident_logs(error_logs: List[Dict[str, Any]]) -> str:
    client = ObservabilityClient()
    model_id = "amazon.titan-text-express-v1"  # Amazon Titan model for text generation

    if not error_logs:
        return "No error logs provided for summarization."

    log_messages = [log.get("@message", "") for log in error_logs]
    combined_logs = "\n".join(log_messages)

    prompt = f"""Analyze the following error logs and provide a concise summary suitable for an incident review. Highlight key issues, frequency, and potential impact. If correlation IDs are present, mention any patterns. Also, suggest potential next steps for investigation. Focus only on the content of the logs. \n\nLogs:\n{combined_logs}\n\nSummary:"""

    body = {
        "inputText": prompt,
        "textGenerationConfig": {
            "maxTokenCount": 500,
            "stopSequences": [],
            "temperature": 0.7,
            "topP": 0.9,
        },
    }

    print(
        f"Summarizing {len(error_logs)} error logs using Amazon Bedrock ({model_id})..."
    )

    try:
        response_body = client.invoke_bedrock_model(model_id, body)
        summary = response_body.get("results")[0].get("outputText")
        print("Incident summary generated successfully.")
        return summary
    except Exception as e:
        print(f"Error generating incident summary: {e}")
        return f"Failed to generate summary due to an error: {e}"


if __name__ == "__main__":
    # Example usage (you would typically pass logs obtained from query_error_logs.py)
    # Ensure AWS_REGION environment variable is set
    # Example: export AWS_REGION=us-east-1

    sample_error_logs = [
        {
            "@timestamp": "2023-10-27 10:00:00.123",
            "@message": '{"level":"ERROR","service":"payment-gateway","message":"Failed to process payment for order ABC-123. Reason: Insufficient funds.","metadata":{"level":"ERROR","service":"payment-gateway"}}',
        },
        {
            "@timestamp": "2023-10-27 10:01:05.456",
            "@message": '{"level":"ERROR","service":"user-profile","message":"Database connection error: Timeout fetching user 456.","metadata":{"level":"ERROR","service":"user-profile"}}',
        },
        {
            "@timestamp": "2023-10-27 10:02:10.789",
            "@message": '{"level":"ERROR","service":"payment-gateway","message":"Failed to process payment for order DEF-456. Reason: Payment service unavailable.","metadata":{"level":"ERROR","service":"payment-gateway"}}',
        },
        {
            "@timestamp": "2023-10-27 10:03:15.111",
            "@message": '{"level":"WARN","service":"user-auth","message":"Multiple failed login attempts for user alice.","metadata":{"level":"WARN","service":"user-auth"}}',
        },  # This one might be filtered out by prompt
    ]

    summary = summarize_incident_logs(sample_error_logs)
    print("\n--- Incident Summary ---")
    print(summary)
