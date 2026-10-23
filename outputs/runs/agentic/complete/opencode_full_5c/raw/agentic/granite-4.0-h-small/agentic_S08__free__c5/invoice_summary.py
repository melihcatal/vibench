# provider: Azure Form Recognizer (continued)

from typing import List
from pydantic import BaseModel
from invoice_note_translate import translate_text
from document_models import NormalizedExpense, InvoiceFieldsResponse


class SummaryItem(BaseModel):
    description: str = Field(..., description="Item description from line items")
    quantity: str = Field(..., description="Quantity purchased")
    unit_price: str = Field(..., description="Unit price as string")
    total: str = Field(..., description="Line item total")


class InvoiceSummary(BaseModel):
    invoice_id: str = Field(..., description="Unique identifier for the invoice")
    vendor: str = Field(..., description="Payee name")
    date: str = Field(..., description="Invoice date as YYYY-MM-DD")
    total_amount: str = Field(..., description="Overall invoice total")
    line_items: List[SummaryItem] = Field(
        ..., description="Detailed items for the invoice"
    )
    confidence: float = Field(
        ..., ge=0, le=1, description="Overall extraction confidence"
    )


def summarize_invoice(extracted: InvoiceFieldsResponse) -> InvoiceSummary:
    """Create a concise summary after extraction and optional moderation/translation."""
    summary_items = []
    if extracted.line_items:
        for item in extracted.line_items:
            # Example assumes line item dicts contain description, quantity, unit_price, total
            summary_items.append(
                SummaryItem(
                    description=item.get("description", "N/A"),
                    quantity=item.get("quantity", "1"),
                    unit_price=item.get("unit_price", "0"),
                    total=item.get("total", "0"),
                )
            )

    return InvoiceSummary(
        invoice_id=extracted.date or "unknown-id",  # fallback; ideally use a proper ID
        vendor=extracted.vendor or "Unknown Vendor",
        date=extracted.date or "1900-01-01",
        total_amount=extracted.total or "0",
        line_items=summary_items,
        confidence=float(extracted.overall_confidence.split("_")[-1])
        if isinstance(extracted.overall_confidence, str)
        else extracted.overall_confidence,
    )


if __name__ == "__main__":
    # Demo summarization using a pre‑populated InvoiceFieldsResponse
    demo_invoice = InvoiceFieldsResponse(
        vendor="Acme Corp",
        date="2024-07-10",
        total="$250.00",
        line_items=[
            {
                "description": "Widget A",
                "quantity": "2",
                "unit_price": "$50",
                "total": "$100",
            },
            {
                "description": "Widget B",
                "quantity": "1",
                "unit_price": "$150",
                "total": "$150",
            },
        ],
        overall_confidence="high",
    )
    summary = summarize_invoice(demo_invoice)
    print("Invoice summary created:")
    print(summary.json(indent=2))
