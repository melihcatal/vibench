import os
from typing import List, Dict
from observability_models import QueryResult, SafetyCheck, EmbedResponse
from observability_client import get_log_client


def summarize_error_logs(error_logs: List[QueryResult]) -> Dict[str, any]:
    """Produce a concise incident‑review summary from a collection of error logs.

    The concrete provider used here is Amazon Bedrock (Amazon Nova/Titan) for summarization.
    """
    # 1. Extract concise messages
    messages = [log["message"] for log in error_logs]
    # 2. Run Bedrock summarization (via boto3) – placeholder SDK call
    bedrock = (
        get_bedrock_client()
    )  # configured via AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
    response = bedrock.summarize(input_text="\\n".join(messages), output_format="text")
    summary = response.get("summary", "[no summary returned]")
    # 3. Return a simple structured summary
    return {"total_errors": len(error_logs), "summary": summary}


# Minimal Bedrock client helper (placeholder for the real SDK) – not imported in other modules
def get_bedrock_client():
    import boto3

    return boto3.client("bedrock-runtime")
