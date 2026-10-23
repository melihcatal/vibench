"""
Summarize message processing results using OpenAI GPT via the OpenAI API.

Uses the openai SDK to call GPT-4o-mini for generating summaries
of message processing outcomes.
Requires OPENAI_API_KEY environment variable for authentication.
"""

import os
import json
from typing import Optional, Sequence

from openai import OpenAI

from messaging_models import PublishResult, BatchPublishResult, ConsumedMessage


OPENAI_MODEL = "gpt-4o-mini"


def summarize_processing_results(
    results: Sequence[dict],
    context: str = "",
    api_key: Optional[str] = None,
) -> str:
    """
    Generate a summary of message processing results using OpenAI GPT-4o-mini.

    Args:
        results: Sequence of processing result dictionaries to summarize.
        context: Additional context about the processing pipeline.
        api_key: Optional OpenAI API key (falls back to OPENAI_API_KEY env var).

    Returns:
        Summary text of the processing results.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=key)

    results_json = json.dumps(results, indent=2)

    system_prompt = (
        "You are a message processing summarizer. "
        "Analyze the provided processing results and generate a concise summary. "
        "Include success/failure counts, common error patterns, and recommendations."
    )

    user_prompt = f"""
Context: {context}

Processing Results:
{results_json}

Please provide a clear summary of these results.
"""

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )

    return response.choices[0].message.content


def summarize_batch_result(
    batch_result: BatchPublishResult,
    topic_id: str = "",
    api_key: Optional[str] = None,
) -> str:
    """
    Summarize a batch publish result using OpenAI GPT-4o-mini.

    Args:
        batch_result: The BatchPublishResult to summarize.
        topic_id: The topic that was published to.
        api_key: Optional OpenAI API key.

    Returns:
        Summary text of the batch result.
    """
    results_data = {
        "topic_id": topic_id,
        "total_sent": batch_result.total_sent,
        "total_failed": batch_result.total_failed,
        "details": batch_result.to_dict()["results"],
    }
    return summarize_processing_results(
        results=[results_data],
        context=f"Batch publish to topic: {topic_id}",
        api_key=api_key,
    )


def summarize_consumed_messages(
    messages: Sequence[ConsumedMessage],
    subscription_id: str = "",
    api_key: Optional[str] = None,
) -> str:
    """
    Summarize consumed messages using OpenAI GPT-4o-mini.

    Args:
        messages: Sequence of consumed messages.
        subscription_id: The subscription messages were consumed from.
        api_key: Optional OpenAI API key.

    Returns:
        Summary text of the consumed messages.
    """
    messages_data = [
        {
            "message_id": m.message_id,
            "event_type": m.attributes.get("event_type", "unknown"),
            "acknowledged": m.acknowledged,
        }
        for m in messages
    ]
    return summarize_processing_results(
        results=messages_data,
        context=f"Messages consumed from subscription: {subscription_id}",
        api_key=api_key,
    )


if __name__ == "__main__":
    sample_results = [
        {"success": True, "message_id": "msg_001", "event_type": "user.signup"},
        {"success": True, "message_id": "msg_002", "event_type": "order.create"},
        {"success": False, "message_id": "msg_003", "error": "Timeout"},
    ]
    summary = summarize_processing_results(sample_results)
    print(summary)
