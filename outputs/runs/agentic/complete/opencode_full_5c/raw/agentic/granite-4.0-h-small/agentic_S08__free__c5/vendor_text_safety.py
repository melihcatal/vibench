# provider: Azure Form Recognizer (optional moderation extension)

from document_models import InvoiceFieldsResponse, ModerationResult
from typing import Optional


def moderate_vendor_note(extracted: InvoiceFieldsResponse) -> InvoiceFieldsResponse:
    """Check vendor/memo field for disallowed content and flag as unsafe if needed."""
    # Placeholder moderator logic - real implementation would call an external moderation API
    VENDOR_NOTE = extracted.vendor
    if VENDOR_NOTE and "unsafe" in VENDOR_NOTE.lower():
        return InvoiceFieldsResponse(
            **extracted.dict(),
            vendor=Optional[str](VENDOR_NOTE),
            moderation=ModerationResult(
                content=VENDOR_NOTE,
                is_safe=False,
                reason="Contains prohibited term 'unsafe'",
            ),
        )
    else:
        return InvoiceFieldsResponse(
            **extracted.dict(),
            moderation=ModerationResult(
                content=VENDOR_NOTE or "",
                is_safe=True,
                reason=None,
            ),
        )


if __name__ == "__main__":
    # Simple manual test
    sample = InvoiceFieldsResponse(
        vendor="Acme Corp (unsafe note here)",
        date="2024-07-10",
        total="$250.00",
        line_items=[],
        overall_confidence="high",
    )
    moderated = moderate_vendor_note(sample)
    print("Moderated result:")
    print(moderated.json(indent=2))
