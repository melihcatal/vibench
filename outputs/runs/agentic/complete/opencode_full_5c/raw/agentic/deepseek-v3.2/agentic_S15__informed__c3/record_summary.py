import os
import json
from typing import Dict, Any, List
from anthropic import Anthropic


def summarize_records(
    records: List[Dict[str, Any]], summary_type: str = "brief"
) -> Dict[str, Any]:
    """
    Summarize retrieved document records using Anthropic Claude.

    Args:
        records: List of document records to summarize
        summary_type: Type of summary ("brief", "detailed", "key_points")

    Returns:
        dict: Summary results
    """
    try:
        # Anthropic API configuration
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY environment variable is required")

        client = Anthropic(api_key=api_key)

        # Prepare records for summarization
        records_text = json.dumps(records, indent=2)

        # Create prompt based on summary type
        if summary_type == "brief":
            system_prompt = "You are a helpful assistant that creates concise summaries of document records."
            user_prompt = f"Please provide a brief summary of these {len(records)} document records:\n\n{records_text}"
        elif summary_type == "detailed":
            system_prompt = "You are a detailed analyst that creates comprehensive summaries of document records."
            user_prompt = f"Please provide a detailed summary of these {len(records)} document records, including key patterns and insights:\n\n{records_text}"
        elif summary_type == "key_points":
            system_prompt = (
                "You are an analyst that extracts key points from document records."
            )
            user_prompt = f"Please extract the key points from these {len(records)} document records as bullet points:\n\n{records_text}"
        else:
            system_prompt = (
                "You are a helpful assistant that summarizes document records."
            )
            user_prompt = f"Please summarize these {len(records)} document records:\n\n{records_text}"

        # Call Anthropic Claude API
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.3,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        summary = response.content[0].text

        return {
            "success": True,
            "summary": summary,
            "summary_type": summary_type,
            "record_count": len(records),
            "model": "claude-3-sonnet-20240229",
            "provider": "Anthropic",
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "record_count": len(records),
            "summary_type": summary_type,
            "provider": "Anthropic",
        }
