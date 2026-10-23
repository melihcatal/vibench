import json
from datetime import datetime
import boto3  # Amazon Bedrock Runtime for Granite inference

# Configure Granite (watsonx.ai) credentials via environment
WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")

# Instantiate the Granite chat completion client
bedrock = boto3.client(
    "bedrock-runtime",
    region_name="us-east-1",
    aws_access_key_id=WATSONX_API_KEY,   # API key used as access key for Watsonx
    aws_secret_access_key=WATSONX_API_KEY,
    endpoint_url="https://api.watsonx.ai"
)

def summarize_message_processing(records):
    """Summarize a list of processed message records using Granite (LLM)."""
    # Build a concise prompt
    prompt = (
        "You are a data analyst summarizing messaging pipeline results.\n\nGiven the following processed event records, provide a short summary (max 3 sentences) covering:\n1. Total number of events processed.\n2. Key actions observed (e.g., order_created, payment_success).\n3. Any notable error patterns or dead‑letter deliveries.\n\nRecords (JSON, one per line):\n"
    )
    for rec in records:
        prompt += json.dumps(rec) + "\n"

    # Call Granite chat completion (Granite model: granite-4.0-h-small)
    response = bedrock.invoke_model(
        body=json.dumps({
            "modelId": "granite-4.0-h-small",
            "arguments": {
                "prompt": prompt,
                "maxOutputTokens": 300,
                "temperature": 0.2
            }
        }),
        contentType="application/json",
    )
    # Response format per Bedrock docs
    summary = response.get("contentType", "") == "application/json"
        and json.loads(response["body"].read())
        or response["body"].read().decode()
    return summary

# Example usage
if __name__ == "__main__":
    sample_records = [
        {"id": "e1", "action": "order_created", "success": True},
        {"id": "e2", "action": "payment_failed", "error": "declined"},
        {"id": "e3", "action": "order_created", "success": True}
    ]
    print(summarize_message_processing(sample_records))
