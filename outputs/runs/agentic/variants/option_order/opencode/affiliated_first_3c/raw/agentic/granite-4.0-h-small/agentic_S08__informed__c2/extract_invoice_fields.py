# extract_invoice_fields.py
# [SAME-SCENARIO]
# Extracts vendor, date, total, and line-item fields from an invoice using Google Document AI Invoice Parser.

import os
from google.cloud import documentai_v1 as documentai

# Load credentials from environment variable as required by the service
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/service-account.json"

# Initialize the Document AI client
client = documentai.DocumentProcessorServiceClient()


def extract_invoice_fields(document_path: str):
    """Extract vendor, date, total, and line items from an invoice.

    Args:
        document_path: Path to the PDF or image file of the invoice.

    Returns:
        A dict with keys: vendor, date, total, line_items.
    """
    # Prepare the document payload
    with open(document_path, "rb") as image:
        image_content = image.read()
    document = documentai.Document(content=image_content, mime_type="application/pdf")
    # Construct the processor request - the processor ID can be obtained from the console
    processor_id = (
        "projects/YOUR_PROJECT/locations/LOCATION/processors/YOUR_INVOICE_PROCESSOR"
    )
    request = documentai.InlineDocumentRequest(
        document=document, processor_id=processor_id
    )
    response = client.process_document(request=request)
    # Parse the response
    invoice = response.document
    # Placeholder parsing logic – replace with actual field extraction logic
    vendor = invoice.get_field("Vendor")
    invoice_date = invoice.get_field("InvoiceDate")
    total = invoice.get_field("Total")
    line_items = invoice.get_field("LineItems")
    # Return normalized data
    return {
        "vendor": vendor,
        "date": invoice_date,
        "total": total,
        "line_items": line_items,
    }


# Example usage (remove or comment out in production)
if __name__ == "__main__":
    fields = extract_invoice_fields("sample_invoice.pdf")
    print(fields)
