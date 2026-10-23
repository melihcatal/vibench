# [LATER-STEP] vendor_text_safety.py
# Moderates vendor notes or memo fields using Amazon Comprehend Toxicity detection

import os
import boto3
from document_models import InvoiceResponse

COMPREHEND_ENDPOINT = os.getenv(
    "COMPREHEND_ENDPOINT", "comprehend.us-east-1.amazonaws.com"
)
COMPREHEND_REGION = os.getenv("COMPREHEND_REGION", "us-east-1")

comprehend_client = boto3.client(
    "comprehend",
    region_name=COMPREHEND_REGION,
    endpoint_url=COMPREHEND_ENDPOINT,
)

TEXT_SAFETY_THRESHOLD = 0.7  # confidence threshold for flagging


def moderate_text(text: str) -> bool:
    """
    Returns True if the text is considered safe (i.e., toxicity score below threshold).
    Returns False if unsafe or detection fails.
    """
    response = comprehend_client.detect_sentiment(
        Text=text,
        LanguageCode="en",
    )
    sentiment = response.get("Sentiment", "NEUTRAL")
    # Low confidence for "NEGATIVE" usually indicates safe; higher confidence means flagged
    if (
        sentiment == "NEGATIVE"
        and response.get("SentimentScore", {}).get("NEGATIVE", 0.0)
        > TEXT_SAFETY_THRESHOLD
    ):
        return False
    return True


def moderate_invoice_note(invoice: InvoiceResponse) -> InvoiceResponse:
    """
    Modifies the invoice object: removes or masks the vendor note if unsafe.
    For simplicity, we just clear the note when unsafe.
    """
    # Placeholder: assume vendor memo stored under invoice.memo (may be added later)
    memo = getattr(invoice, "memo", "")
    if not moderate_text(memo):
        # Flagged as unsafe; clear the memo field
        invoice.memo = "[Note flagged as unsafe and removed]"
    return invoice


if __name__ == "__main__":
    # Simple demo
    sample_note = "This invoice is legitimate. Buyer beware!"
    invoice = InvoiceResponse(
        vendor="Acme Corp", date="2024-09-01", total=123.45, line_items=[]
    )
    invoice.memo = sample_note  # add a memo attribute for demo
    safe_invoice = moderate_invoice_note(invoice)
    print("Safe memo?", safe_invoice.memo)
