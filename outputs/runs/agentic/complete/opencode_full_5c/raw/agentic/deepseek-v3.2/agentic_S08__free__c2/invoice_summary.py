import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from document_models import (
    InvoiceExtractionResult,
    NormalizedExpense,
    ExpenseSummary,
    ExpenseCategory,
)


def summarize_invoice_fields(
    invoice_result: InvoiceExtractionResult,
    normalized_expense: Optional[NormalizedExpense] = None,
) -> ExpenseSummary:
    """
    Summarize extracted invoice fields using Anthropic Claude.
    """
    try:
        from document_client import get_anthropic_client

        client = get_anthropic_client()

        vendor = invoice_result.vendor
        total_amount = invoice_result.total_amount
        date = invoice_result.invoice_date
        line_items = invoice_result.line_items

        try:
            amount_float = float(total_amount) if total_amount else 0.0
        except:
            amount_float = 0.0

        line_item_count = len(line_items)

        category = ExpenseCategory.OTHER
        if normalized_expense:
            category = normalized_expense.category

        prompt = f"""
        Summarize this invoice transaction for expense reporting:
        
        Vendor: {vendor}
        Total Amount: ${amount_float:.2f}
        Invoice Date: {date}
        Number of Line Items: {line_item_count}
        Category: {category.value}
        
        Line Items (first 3):
        {json.dumps(line_items[:3], indent=2) if line_items else "No line items"}
        
        Please provide a concise 2-3 sentence summary that includes:
        1. What the expense was for
        2. Key details about the vendor and transaction
        3. Any notable aspects of the line items
        
        Return ONLY the summary text, no additional formatting or labels.
        """

        response = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=150,
            temperature=0.3,
            messages=[{"role": "user", "content": prompt}],
        )

        summary_text = response.content[0].text.strip()

        date_range = None
        if date:
            date_range = {"start": date, "end": date}

        return ExpenseSummary(
            vendor=vendor,
            total_amount=amount_float,
            category=category,
            line_item_count=line_item_count,
            date_range=date_range,
            summary_text=summary_text,
            provider="anthropic",
            model_used="claude-3-haiku-20240307",
            metadata={
                "summary_type": "invoice",
                "source_provider": invoice_result.provider,
                "line_items_available": len(line_items) > 0,
            },
        )

    except Exception as e:
        raise Exception(f"Anthropic Claude summarization failed: {str(e)}")
