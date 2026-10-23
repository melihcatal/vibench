"""
Summarize extracted invoice fields using OpenAI GPT-4.
Provider: OpenAI Chat Completions API (gpt-4 model)
"""

import os
import json
from typing import Optional, List, Dict, Any
from openai import OpenAI

from document_models import InvoiceExtractionResponse, InvoiceSummary, LineItem


def summarize_invoice(
    invoice_data: InvoiceExtractionResponse,
    additional_notes: Optional[str] = None,
    api_key: Optional[str] = None,
    model: str = "gpt-4",
) -> InvoiceSummary:
    """
    Generate a human-readable summary of extracted invoice fields using OpenAI GPT-4.
    
    Uses the gpt-4 model to produce a structured summary of invoice data including
    vendor information, dates, amounts, and line item breakdowns.
    
    Args:
        invoice_data: InvoiceExtractionResponse from extract_invoice_fields
        additional_notes: Optional additional context or notes
        api_key: OpenAI API key
        model: OpenAI model ID (default: gpt-4)
    
    Returns:
        InvoiceSummary with structured summary data
    """
    client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
    
    line_items_data = []
    for item in invoice_data.line_items:
        line_items_data.append({
            "description": item.description,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "line_total": item.line_total,
        })
    
    prompt = _build_summary_prompt(invoice_data, line_items_data, additional_notes)
    
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an invoice analysis assistant. Given extracted invoice data, "
                        "produce a structured JSON summary. Only return valid JSON with no "
                        "additional text or markdown."
                    ),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0.1,
            response_format={"type": "json_object"},
        )
        
        content = response.choices[0].message.content
        if content:
            parsed = json.loads(content)
            return InvoiceSummary(
                vendor=parsed.get("vendor", invoice_data.vendor),
                invoice_date=parsed.get("invoice_date", invoice_data.invoice_date),
                total_amount=parsed.get("total_amount", invoice_data.total_amount),
                line_item_count=parsed.get("line_item_count", len(invoice_data.line_items)),
                line_item_total=parsed.get("line_item_total"),
                has_missing_fields=parsed.get("has_missing_fields", False),
                missing_fields=parsed.get("missing_fields", []),
            )
    except Exception as e:
        pass
    
    return _build_fallback_summary(invoice_data)


def summarize_invoices_batch(
    invoices: List[InvoiceExtractionResponse],
    api_key: Optional[str] = None,
    model: str = "gpt-4",
) -> List[InvoiceSummary]:
    """
    Summarize a batch of invoices using OpenAI GPT-4.
    
    Args:
        invoices: List of InvoiceExtractionResponse objects
        api_key: OpenAI API key
        model: OpenAI model ID (default: gpt-4)
    
    Returns:
        List of InvoiceSummary objects
    """
    summaries: List[InvoiceSummary] = []
    for invoice in invoices:
        summary = summarize_invoice(invoice, api_key=api_key, model=model)
        summaries.append(summary)
    return summaries


def _build_summary_prompt(
    invoice: InvoiceExtractionResponse,
    line_items: List[Dict[str, Any]],
    additional_notes: Optional[str],
) -> str:
    """Build the prompt text for invoice summarization."""
    prompt = f"""Summarize the following invoice data as a JSON object with these exact keys:
- "vendor": vendor name string
- "invoice_date": invoice date string
- "total_amount": total amount as a number
- "line_item_count": number of line items as an integer
- "line_item_total": sum of line item totals as a number
- "has_missing_fields": boolean indicating if key fields are missing
- "missing_fields": array of field names that are missing or empty

Invoice Data:
- Vendor: {invoice.vendor or 'N/A'}
- Date: {invoice.invoice_date or 'N/A'}
- Total Amount: {invoice.total_amount or 'N/A'}
- Vendor Confidence: {invoice.vendor_confidence}
- Date Confidence: {invoice.date_confidence}
- Total Confidence: {invoice.total_confidence}
- Line Items: {json.dumps(line_items, indent=2)}
"""
    if additional_notes:
        prompt += f"\nAdditional Notes: {additional_notes}\n"
    
    return prompt


def _build_fallback_summary(invoice: InvoiceExtractionResponse) -> InvoiceSummary:
    """Build a fallback summary without LLM assistance."""
    missing = []
    if not invoice.vendor:
        missing.append("vendor")
    if not invoice.invoice_date:
        missing.append("invoice_date")
    if invoice.total_amount is None:
        missing.append("total_amount")
    
    line_total = sum(
        item.line_total or 0.0
        for item in invoice.line_items
        if isinstance(item.line_total, (int, float))
    )
    
    return InvoiceSummary(
        vendor=invoice.vendor,
        invoice_date=invoice.invoice_date,
        total_amount=invoice.total_amount,
        line_item_count=len(invoice.line_items),
        line_item_total=line_total if line_total > 0 else invoice.total_amount,
        has_missing_fields=len(missing) > 0,
        missing_fields=missing,
    )


if __name__ == "__main__":
    from document_models import InvoiceExtractionResponse, LineItem
    
    sample = InvoiceExtractionResponse(
        vendor="Office Supply Co.",
        invoice_date="2024-01-15",
        total_amount=250.00,
        line_items=[
            LineItem(description="Paper Reams", quantity=10, unit_price=12.0, line_total=120.0),
            LineItem(description="Printer Cartridges", quantity=3, unit_price=40.0, line_total=120.0),
        ],
        vendor_confidence=0.95,
        date_confidence=0.90,
        total_confidence=0.92,
    )
    
    summary = summarize_invoice(sample)
    print(summary.model_dump_json(indent=2))
