"""
Summarize message processing results.

Provider: OpenAI Chat Completions API
SDK: openai
Interface: SDK
Auth: OPENAI_API_KEY
Model: gpt-4o-mini
"""

import json
import os
from typing import Any, Dict, List, Optional

from openai import OpenAI
from openai import APIError, APITimeoutError, RateLimitError

from messaging_models import (
    EventMessage,
    ProcessingSummary,
    ConsumeResponse,
    PublishResponse,
)


def summarize_processing_results(
    messages: List[Dict[str, Any]],
    processing_stats: Optional[Dict[str, int]] = None,
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
) -> ProcessingSummary:
    """
    Generate a summary of message processing results using OpenAI GPT-4o-mini.

    Args:
        messages: List of processed message data.
        processing_stats: Optional statistics about processing.
        model: OpenAI model identifier (default: gpt-4o-mini).
        api_key: Optional OpenAI API key.

    Returns:
        ProcessingSummary with AI-generated summary text.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY", "")

    try:
        client = OpenAI(api_key=key)

        messages_context = json.dumps(messages, default=str)[:8000]
        stats_context = json.dumps(processing_stats, default=str) if processing_stats else "none"

        prompt = (
            f"Analyze the following message processing results and provide a concise summary.\n\n"
            f"Processing statistics: {stats_context}\n\n"
            f"Sample messages processed: {messages_context}\n\n"
            f"Provide a summary that includes:\n"
            f"1. Overall processing health assessment\n"
            f"2. Key patterns observed in the messages\n"
            f"3. Any anomalies or issues detected\n"
            f"4. Recommendations for improving message processing\n\n"
            f"Keep the summary under 200 words."
        )

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a messaging system analyst. "
                        "Provide concise, technical summaries of message processing results."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=500,
            temperature=0.3,
        )

        summary_text = response.choices[0].message.content.strip()

        successful = processing_stats.get("successful", 0) if processing_stats else 0
        failed = processing_stats.get("failed", 0) if processing_stats else 0
        dead_lettered = processing_stats.get("dead_lettered", 0) if processing_stats else 0
        total = len(messages) if messages else successful + failed + dead_lettered

        return ProcessingSummary(
            total_messages=total,
            successful=successful,
            failed=failed,
            dead_lettered=dead_lettered,
            summary_text=summary_text,
            details=messages[:50],
        )

    except RateLimitError as e:
        return ProcessingSummary(
            total_messages=len(messages) if messages else 0,
            successful=processing_stats.get("successful", 0) if processing_stats else 0,
            failed=processing_stats.get("failed", 0) if processing_stats else 0,
            dead_lettered=processing_stats.get("dead_lettered", 0) if processing_stats else 0,
            summary_text=f"OpenAI rate limit exceeded: {str(e)}",
        )
    except APITimeoutError as e:
        return ProcessingSummary(
            total_messages=len(messages) if messages else 0,
            successful=processing_stats.get("successful", 0) if processing_stats else 0,
            failed=processing_stats.get("failed", 0) if processing_stats else 0,
            dead_lettered=processing_stats.get("dead_lettered", 0) if processing_stats else 0,
            summary_text=f"OpenAI API timeout: {str(e)}",
        )
    except APIError as e:
        return ProcessingSummary(
            total_messages=len(messages) if messages else 0,
            successful=processing_stats.get("successful", 0) if processing_stats else 0,
            failed=processing_stats.get("failed", 0) if processing_stats else 0,
            dead_lettered=processing_stats.get("dead_lettered", 0) if processing_stats else 0,
            summary_text=f"OpenAI API error: {str(e)}",
        )
    except Exception as e:
        return ProcessingSummary(
            total_messages=len(messages) if messages else 0,
            successful=processing_stats.get("successful", 0) if processing_stats else 0,
            failed=processing_stats.get("failed", 0) if processing_stats else 0,
            dead_lettered=processing_stats.get("dead_lettered", 0) if processing_stats else 0,
            summary_text=f"Failed to generate summary: {str(e)}",
        )


def summarize_single_event(
    event: EventMessage,
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
) -> str:
    """
    Generate a summary for a single event using OpenAI GPT-4o-mini.

    Args:
        event: The EventMessage to summarize.
        model: OpenAI model identifier.
        api_key: Optional OpenAI API key.

    Returns:
        Summary text for the event.
    """
    key = api_key or os.environ.get("OPENAI_API_KEY", "")

    try:
        client = OpenAI(api_key=key)

        payload_str = json.dumps(event.payload, default=str)[:4000]

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a data analyst. Provide a one-sentence summary "
                        "of the following event payload."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Event type: {event.event_type}\nPayload: {payload_str}",
                },
            ],
            max_tokens=100,
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Failed to summarize: {str(e)}"
