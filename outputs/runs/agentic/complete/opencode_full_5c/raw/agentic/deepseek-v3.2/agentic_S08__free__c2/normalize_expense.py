import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime
from document_models import (
    InvoiceExtractionResult,
    ReceiptExtractionResult,
    NormalizedExpense,
    ExpenseCategory,
)


def normalize_expense(
    extraction_result: InvoiceExtractionResult | ReceiptExtractionResult,
    category_hint: Optional[str] = None,
) -> NormalizedExpense:
    """
    Normalize extracted expense fields into a standard JSON schema using OpenAI GPT for categorization.
    """
    try:
        import openai

        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

        if isinstance(extraction_result, InvoiceExtractionResult):
            vendor = extraction_result.vendor
            amount_str = extraction_result.total_amount
            date_str = extraction_result.invoice_date

            try:
                amount = float(amount_str) if amount_str else 0.0
            except:
                amount = 0.0

            try:
                date = (
                    datetime.fromisoformat(date_str.replace("Z", "+00:00"))
                    if date_str
                    else datetime.now()
                )
            except:
                date = datetime.now()

            description = f"Invoice from {vendor}"
            line_items = extraction_result.line_items

        elif isinstance(extraction_result, ReceiptExtractionResult):
            vendor = extraction_result.merchant
            amount = extraction_result.total_amount or 0.0
            date = datetime.now()
            description = f"Receipt from {vendor}"
            line_items = [
                {
                    "name": item.get("name", ""),
                    "price": item.get("price", 0.0),
                    "quantity": item.get("quantity", 1),
                }
                for item in extraction_result.items
            ]
        else:
            raise ValueError("Unsupported extraction result type")

        prompt = f"""
        Categorize this expense transaction:
        Vendor: {vendor}
        Amount: ${amount:.2f}
        Description: {description}
        
        Available categories: {[cat.value for cat in ExpenseCategory]}
        
        Return ONLY a JSON object with this exact structure:
        {{
            "category": "one_of_the_available_categories",
            "subcategory": "specific_subcategory_or_null",
            "tags": ["tag1", "tag2", "tag3"]
        }}
        """

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expense categorization assistant. Return only valid JSON.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.1,
            max_tokens=100,
        )

        categorization = json.loads(response.choices[0].message.content)

        category = ExpenseCategory(categorization["category"])
        subcategory = categorization.get("subcategory")
        tags = categorization.get("tags", [])

        if category_hint:
            tags.append(category_hint)

        normalized = NormalizedExpense(
            vendor=vendor,
            amount=amount,
            date=date.isoformat(),
            description=description,
            category=category,
            subcategory=subcategory,
            tags=tags,
            line_items=line_items,
            source_provider=extraction_result.provider,
            source_model=extraction_result.model_used,
            confidence_scores=extraction_result.confidence_scores,
            metadata={
                "normalization_timestamp": datetime.now().isoformat(),
                "normalization_provider": "openai",
                "normalization_model": "gpt-3.5-turbo",
            },
        )

        return normalized

    except Exception as e:
        raise Exception(f"OpenAI normalization failed: {str(e)}")
