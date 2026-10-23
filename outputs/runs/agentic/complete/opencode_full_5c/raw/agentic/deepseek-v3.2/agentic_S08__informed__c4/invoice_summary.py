import os
import json
from typing import Dict, Any
from anthropic import Anthropic


def summarize_invoice_fields(invoice_data: Dict[str, Any]) -> Dict[str, Any]:
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("Anthropic API key not configured")

    client = Anthropic(api_key=api_key)

    invoice_json = json.dumps(invoice_data, indent=2)

    prompt = f"""You are an expert financial analyst summarizing invoice data. 
Given the following extracted invoice data, provide a concise summary including:
1. Key vendor information
2. Invoice date and total amount
3. Number of line items and total line item amount
4. Any notable patterns or anomalies

Invoice Data:
{invoice_json}

Provide your summary in JSON format with these fields:
- vendor_summary (string): Brief description of vendor
- date_summary (string): Formatted date information
- total_summary (string): Total amount with context
- line_items_summary (string): Summary of line items
- notable_findings (array of strings): Any notable patterns or issues
- confidence_assessment (string): Assessment of data quality"""

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=500,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}],
        )

        summary_text = response.content[0].text

        try:
            summary_json = json.loads(summary_text)
        except json.JSONDecodeError:
            summary_json = {
                "summary_text": summary_text,
                "vendor": invoice_data.get("vendor"),
                "date": invoice_data.get("date"),
                "total": invoice_data.get("total"),
                "line_item_count": len(invoice_data.get("line_items", [])),
                "extracted_from_response": True,
            }

        return {
            "invoice_summary": summary_json,
            "model_used": "claude-3-5-sonnet-20241022",
            "provider": "anthropic",
            "extraction_confidence": invoice_data.get("confidence"),
        }

    except Exception as e:
        return {
            "error": str(e),
            "fallback_summary": create_fallback_summary(invoice_data),
        }


def create_fallback_summary(invoice_data: Dict[str, Any]) -> Dict[str, Any]:
    line_items = invoice_data.get("line_items", [])
    line_item_total = sum(
        item.get("amount", 0)
        for item in line_items
        if isinstance(item.get("amount"), (int, float))
    )

    return {
        "vendor": invoice_data.get("vendor"),
        "date": invoice_data.get("date"),
        "total_amount": invoice_data.get("total"),
        "line_item_count": len(line_items),
        "line_item_total": line_item_total,
        "discrepancy": abs(invoice_data.get("total", 0) - line_item_total)
        if invoice_data.get("total")
        else None,
        "summary": f"Invoice from {invoice_data.get('vendor', 'Unknown vendor')} dated {invoice_data.get('date', 'Unknown date')} for ${invoice_data.get('total', 0):.2f} with {len(line_items)} line items.",
    }


def summarize_multiple_invoices(invoices_data: list) -> Dict[str, Any]:
    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        raise ValueError("Anthropic API key not configured")

    client = Anthropic(api_key=api_key)

    invoices_json = json.dumps(invoices_data, indent=2)

    prompt = f"""You are an expert financial analyst summarizing multiple invoices. 
Given the following list of extracted invoice data, provide a comprehensive summary including:
1. Total number of invoices
2. Total amount across all invoices
3. Top vendors by total amount
4. Date range of invoices
5. Average invoice amount
6. Any patterns or anomalies across the dataset

Invoice Data:
{invoices_json}

Provide your summary in JSON format with these fields:
- total_invoices (number)
- total_amount (number)
- date_range (object with start_date and end_date)
- top_vendors (array of objects with vendor and total_amount)
- average_invoice_amount (number)
- patterns (array of strings)
- recommendations (array of strings)"""

    try:
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=800,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}],
        )

        summary_text = response.content[0].text

        try:
            summary_json = json.loads(summary_text)
        except json.JSONDecodeError:
            summary_json = {
                "summary_text": summary_text,
                "total_invoices": len(invoices_data),
                "extracted_from_response": True,
            }

        return {
            "batch_summary": summary_json,
            "model_used": "claude-3-5-sonnet-20241022",
            "provider": "anthropic",
            "invoice_count": len(invoices_data),
        }

    except Exception as e:
        return {
            "error": str(e),
            "fallback_summary": create_fallback_batch_summary(invoices_data),
        }


def create_fallback_batch_summary(invoices_data: list) -> Dict[str, Any]:
    if not invoices_data:
        return {"message": "No invoice data provided"}

    total_amount = sum(
        inv.get("total", 0)
        for inv in invoices_data
        if isinstance(inv.get("total"), (int, float))
    )
    vendor_totals = {}

    for invoice in invoices_data:
        vendor = invoice.get("vendor")
        amount = invoice.get("total", 0)
        if vendor:
            vendor_totals[vendor] = vendor_totals.get(vendor, 0) + amount

    top_vendors = sorted(vendor_totals.items(), key=lambda x: x[1], reverse=True)[:5]

    dates = [inv.get("date") for inv in invoices_data if inv.get("date")]
    valid_dates = [d for d in dates if d]

    return {
        "total_invoices": len(invoices_data),
        "total_amount": total_amount,
        "average_invoice_amount": total_amount / len(invoices_data)
        if invoices_data
        else 0,
        "top_vendors": [{"vendor": v, "total_amount": a} for v, a in top_vendors],
        "date_range": {
            "start_date": min(valid_dates) if valid_dates else None,
            "end_date": max(valid_dates) if valid_dates else None,
        },
    }
