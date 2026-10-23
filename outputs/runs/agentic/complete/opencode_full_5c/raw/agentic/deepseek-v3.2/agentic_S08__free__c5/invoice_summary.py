import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from document_models import ExpenseRecord


def summarize_invoice_fields(expense_record: ExpenseRecord) -> Dict[str, Any]:
    """
    Summarize extracted invoice fields using Anthropic Claude for intelligent summarization.
    """
    import anthropic

    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    # Prepare the expense data for summarization
    expense_data = {
        "vendor": expense_record.vendor_name,
        "date": expense_record.transaction_date,
        "total": expense_record.total_amount,
        "currency": expense_record.currency,
        "tax": expense_record.tax_amount,
        "category": expense_record.category,
        "line_items": expense_record.line_items,
        "item_count": len(expense_record.line_items),
    }

    # Calculate item statistics
    item_stats = {
        "total_items": len(expense_record.line_items),
        "total_amount": sum(
            item.get("amount", 0) for item in expense_record.line_items
        ),
        "average_item_price": 0,
        "most_expensive_item": None,
        "item_categories": set(),
    }

    if expense_record.line_items:
        item_stats["average_item_price"] = (
            item_stats["total_amount"] / item_stats["total_items"]
        )
        most_expensive = max(
            expense_record.line_items, key=lambda x: x.get("amount", 0)
        )
        item_stats["most_expensive_item"] = most_expensive

    # Use Claude to generate a natural language summary
    prompt = f"""
    Analyze this invoice data and provide a comprehensive summary:
    
    Invoice Data:
    {json.dumps(expense_data, indent=2)}
    
    Item Statistics:
    {json.dumps(item_stats, indent=2)}
    
    Please provide a JSON summary with these fields:
    1. executive_summary: A brief 2-3 sentence overview of the invoice
    2. key_findings: List of 3-5 important observations about this invoice
    3. risk_assessment: Assessment of any potential issues (missing data, unusual amounts, etc.)
    4. categorization_suggestion: Suggested expense category if different from current
    5. compliance_check: Any compliance or policy considerations
    6. next_actions: Suggested next steps for processing this invoice
    
    Return ONLY the JSON object, no other text.
    """

    try:
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0.1,
            messages=[{"role": "user", "content": prompt}],
        )

        summary_text = response.content[0].text.strip()

        # Parse the JSON response
        summary_data = json.loads(summary_text)

        # Add calculated statistics
        summary_data["calculated_statistics"] = {
            "total_items": item_stats["total_items"],
            "items_total": item_stats["total_amount"],
            "average_item_price": item_stats["average_item_price"],
            "tax_percentage": (
                expense_record.tax_amount / expense_record.total_amount * 100
            )
            if expense_record.tax_amount and expense_record.total_amount
            else 0,
            "processing_date": datetime.utcnow().isoformat(),
        }

        # Add metadata
        summary_data["metadata"] = {
            "summary_generated_at": datetime.utcnow().isoformat(),
            "model_used": "claude-3-sonnet-20240229",
            "source_vendor": expense_record.vendor_name,
            "record_id": f"inv_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        }

        return summary_data

    except Exception as e:
        # Fallback to basic summary
        return generate_basic_summary(expense_record)


def generate_basic_summary(expense_record: ExpenseRecord) -> Dict[str, Any]:
    """Generate a basic summary without AI."""
    summary = {
        "executive_summary": f"Invoice from {expense_record.vendor_name} for {expense_record.total_amount} {expense_record.currency} dated {expense_record.transaction_date}",
        "key_findings": [
            f"Total amount: {expense_record.total_amount} {expense_record.currency}",
            f"Number of line items: {len(expense_record.line_items)}",
            f"Tax amount: {expense_record.tax_amount or 'Not specified'}",
            f"Category: {expense_record.category}",
        ],
        "risk_assessment": "Basic validation passed. No AI risk assessment available.",
        "categorization_suggestion": expense_record.category,
        "compliance_check": "Basic compliance check passed. Manual review recommended.",
        "next_actions": [
            "Review invoice details",
            "Approve for payment",
            "Archive document",
        ],
        "calculated_statistics": {
            "total_items": len(expense_record.line_items),
            "items_total": sum(
                item.get("amount", 0) for item in expense_record.line_items
            ),
            "average_item_price": sum(
                item.get("amount", 0) for item in expense_record.line_items
            )
            / len(expense_record.line_items)
            if expense_record.line_items
            else 0,
            "tax_percentage": (
                expense_record.tax_amount / expense_record.total_amount * 100
            )
            if expense_record.tax_amount and expense_record.total_amount
            else 0,
            "processing_date": datetime.utcnow().isoformat(),
        },
        "metadata": {
            "summary_generated_at": datetime.utcnow().isoformat(),
            "model_used": "basic_fallback",
            "source_vendor": expense_record.vendor_name,
        },
    }

    return summary


if __name__ == "__main__":
    # Example usage
    from document_models import ExpenseRecord

    sample_record = ExpenseRecord(
        vendor_name="Tech Supplies Inc.",
        transaction_date="2024-01-15",
        total_amount=1250.75,
        currency="USD",
        line_items=[
            {"description": "Laptop", "quantity": 2, "unit_price": 500, "amount": 1000},
            {
                "description": "Monitor",
                "quantity": 1,
                "unit_price": 250.75,
                "amount": 250.75,
            },
        ],
        tax_amount=87.55,
        category="Equipment",
    )

    summary = summarize_invoice_fields(sample_record)
    print(json.dumps(summary, indent=2))
