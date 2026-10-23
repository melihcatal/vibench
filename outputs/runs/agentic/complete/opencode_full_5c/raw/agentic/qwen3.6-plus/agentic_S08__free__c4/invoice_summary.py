import os
import json
from typing import Dict, Any, Optional
from openai import OpenAI
from document_client import get_openai_config
from document_models import InvoiceExtraction


OPENAI_MODEL = "gpt-4o"
OPENAI_API_BASE = "https://api.openai.com/v1"


def summarize_invoice_fields(invoice: InvoiceExtraction) -> Dict[str, Any]:
    config = get_openai_config()
    api_key = config["api_key"]
    model = config.get("model", OPENAI_MODEL)
    api_base = config.get("api_base", OPENAI_API_BASE)

    client = OpenAI(api_key=api_key, base_url=api_base)

    invoice_data = {
        "vendor_name": invoice.vendor_name,
        "invoice_date": invoice.invoice_date,
        "invoice_number": invoice.invoice_number,
        "total_amount": invoice.total_amount,
        "tax_amount": invoice.tax_amount,
        "currency": invoice.currency,
        "line_items": [
            {
                "description": item.description,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total": item.total,
            }
            for item in invoice.line_items
        ],
    }

    system_prompt = """You are an invoice summarization assistant. Given structured invoice data, produce a concise JSON summary with key insights including vendor analysis, spending category, payment urgency assessment, and budget impact notes."""

    user_content = json.dumps(invoice_data)

    json_schema = {
        "type": "object",
        "properties": {
            "vendor_name": {"type": "string"},
            "invoice_number": {"type": "string"},
            "invoice_date": {"type": "string"},
            "total_amount": {"type": "number"},
            "currency": {"type": "string"},
            "spending_category": {
                "type": "string",
                "enum": [
                    "office_supplies",
                    "technology",
                    "services",
                    "travel",
                    "utilities",
                    "other",
                ],
            },
            "vendor_type": {"type": "string"},
            "line_item_count": {"type": "integer"},
            "average_item_cost": {"type": "number"},
            "tax_rate_percentage": {"type": "number"},
            "summary_notes": {"type": "string"},
            "risk_flags": {"type": "array", "items": {"type": "string"}},
            "recommended_action": {
                "type": "string",
                "enum": ["approve", "review", "escalate"],
            },
        },
        "required": [
            "vendor_name",
            "invoice_number",
            "total_amount",
            "spending_category",
            "line_item_count",
            "summary_notes",
            "recommended_action",
        ],
    }

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": {
                "name": "invoice_summary",
                "schema": json_schema,
                "strict": True,
            },
        },
    )

    summary = json.loads(response.choices[0].message.content)

    if invoice.total_amount > 0 and invoice.tax_amount > 0:
        calculated_tax_rate = (invoice.tax_amount / invoice.total_amount) * 100
        summary["tax_rate_percentage"] = round(calculated_tax_rate, 2)

    summary["line_item_count"] = len(invoice.line_items)

    if invoice.line_items:
        avg_cost = sum(item.total for item in invoice.line_items) / len(
            invoice.line_items
        )
        summary["average_item_cost"] = round(avg_cost, 2)

    return summary


def summarize_multiple_invoices(invoices: list) -> Dict[str, Any]:
    summaries = []
    for invoice in invoices:
        summary = summarize_invoice_fields(invoice)
        summaries.append(summary)

    total_value = sum(s.get("total_amount", 0) for s in summaries)
    unique_vendors = set(s.get("vendor_name", "") for s in summaries)
    categories = [s.get("spending_category", "other") for s in summaries]
    category_counts = {}
    for cat in categories:
        category_counts[cat] = category_counts.get(cat, 0) + 1

    return {
        "invoice_count": len(summaries),
        "total_value": total_value,
        "unique_vendors": len(unique_vendors),
        "vendor_list": list(unique_vendors),
        "category_breakdown": category_counts,
        "individual_summaries": summaries,
    }


if __name__ == "__main__":
    from document_models import InvoiceExtraction, LineItem

    sample = InvoiceExtraction(
        vendor_name="TechCorp Solutions",
        invoice_date="2024-03-15",
        invoice_number="TC-2024-0892",
        total_amount=4500.00,
        tax_amount=450.00,
        currency="USD",
        line_items=[
            LineItem(
                description="Software licenses",
                quantity=10,
                unit_price=400.0,
                total=4000.0,
            ),
            LineItem(
                description="Support package", quantity=1, unit_price=500.0, total=500.0
            ),
        ],
    )
    result = summarize_invoice_fields(sample)
    print(json.dumps(result, indent=2))
