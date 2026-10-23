"""
Summarize extracted invoice fields using Anthropic Claude via the Messages API.

Provider: Anthropic Messages API
SDK: anthropic
Auth: ANTHROPIC_API_KEY
Model: claude-3-sonnet-20240229
"""

import os
import json
from typing import Dict, Any, Optional, List

from anthropic import Anthropic

from document_models import InvoiceExtractionResult


SYSTEM_PROMPT = (
    "You are an expert invoice summarization assistant. "
    "Given structured invoice extraction data, produce a concise, "
    "human-readable summary of the invoice including vendor, date, "
    "total, tax, and line items."
)

SUMMARIZE_PROMPT_TEMPLATE = (
    "Please summarize the following invoice extraction results in a clear, "
    "structured format. Include:\n"
    "- Vendor name\n"
    "- Invoice number and date\n"
    "- Total amount and tax\n"
    "- Summary of line items\n\n"
    "Extraction data:\n{extraction_data}\n\n"
    "Provide the summary in JSON format with keys: "
    "summary_text, vendor, invoice_number, invoice_date, total, tax, "
    "line_item_summary, key_insights."
)


def summarize_invoice_fields(
    extraction_result: InvoiceExtractionResult,
    model_id: str = "claude-3-sonnet-20240229",
    max_tokens: int = 1024,
    temperature: float = 0.3,
) -> Dict[str, Any]:
    """
    Summarize extracted invoice fields using Anthropic Claude.

    Args:
        extraction_result: The InvoiceExtractionResult to summarize.
        model_id: Anthropic Claude model identifier.
        max_tokens: Maximum tokens for the response.
        temperature: Sampling temperature.

    Returns:
        Dictionary with summary fields from Claude.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY environment variable is not set")

    client = Anthropic(api_key=api_key)

    extraction_data = json.dumps(extraction_result.to_dict(), indent=2, default=str)
    prompt = SUMMARIZE_PROMPT_TEMPLATE.format(extraction_data=extraction_data)

    message = client.messages.create(
        model=model_id,
        max_tokens=max_tokens,
        temperature=temperature,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    response_text = message.content[0].text if message.content else ""

    summary = _parse_summary_response(response_text)
    summary["provider"] = "anthropic"
    summary["model_id"] = model_id
    summary["input_tokens"] = message.usage.input_tokens if message.usage else 0
    summary["output_tokens"] = message.usage.output_tokens if message.usage else 0

    return summary


def summarize_invoice_batch(
    extraction_results: List[InvoiceExtractionResult],
    model_id: str = "claude-3-sonnet-20240229",
    max_tokens: int = 2048,
) -> List[Dict[str, Any]]:
    """
    Summarize a batch of invoice extraction results.

    Args:
        extraction_results: List of InvoiceExtractionResult objects.
        model_id: Anthropic Claude model identifier.
        max_tokens: Maximum tokens for the response.

    Returns:
        List of summary dictionaries.
    """
    summaries = []
    for result in extraction_results:
        summary = summarize_invoice_fields(result, model_id, max_tokens)
        summaries.append(summary)
    return summaries


def generate_invoice_narrative(
    extraction_result: InvoiceExtractionResult,
    model_id: str = "claude-3-sonnet-20240229",
    max_tokens: int = 512,
) -> str:
    """
    Generate a natural-language narrative description of an invoice.

    Args:
        extraction_result: The InvoiceExtractionResult to narrate.
        model_id: Anthropic Claude model identifier.
        max_tokens: Maximum tokens.

    Returns:
        Natural-language narrative string.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY environment variable is not set")

    client = Anthropic(api_key=api_key)

    extraction_data = json.dumps(extraction_result.to_dict(), indent=2, default=str)
    prompt = (
        f"Write a short, professional narrative summary of this invoice for "
        f"an expense report. Include the vendor, date, total, and a brief "
        f"description of the purchased items.\n\n"
        f"Invoice data:\n{extraction_data}"
    )

    message = client.messages.create(
        model=model_id,
        max_tokens=max_tokens,
        temperature=0.5,
        system="You write professional expense report summaries.",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    return message.content[0].text if message.content else ""


def _parse_summary_response(response_text: str) -> Dict[str, Any]:
    """Parse the JSON summary from the Claude response."""
    # Try to extract JSON from the response
    text = response_text.strip()

    # Handle markdown code block wrapping
    if text.startswith("```"):
        text = text.split("\n", 1)[-1]
        if text.endswith("```"):
            text = text[:-3].strip()

    try:
        summary = json.loads(text)
        if isinstance(summary, dict):
            return summary
    except json.JSONDecodeError:
        pass

    # Try to find JSON within the text
    start_idx = text.find("{")
    end_idx = text.rfind("}")
    if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
        try:
            summary = json.loads(text[start_idx : end_idx + 1])
            if isinstance(summary, dict):
                return summary
        except json.JSONDecodeError:
            pass

    # Fallback: return as a single text field
    return {
        "summary_text": response_text.strip(),
        "vendor": None,
        "invoice_number": None,
        "invoice_date": None,
        "total": None,
        "tax": None,
        "line_item_summary": None,
        "key_insights": None,
    }
