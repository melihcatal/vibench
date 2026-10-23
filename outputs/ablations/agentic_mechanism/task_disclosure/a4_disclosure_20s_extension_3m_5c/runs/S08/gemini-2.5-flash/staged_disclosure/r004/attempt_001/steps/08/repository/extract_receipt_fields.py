import io
from google.cloud import vision

def extract_receipt_fields(image_path):
    """
    Extracts merchant, tax, total, and items from a receipt image using Google Cloud Vision API.
    """
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    full_text = response.full_text_annotation.text

    # Placeholder for extraction logic
    merchant_name = "Not Found"
    tax_amount = 0.0
    total_amount = 0.0
    items = []

    # In a real-world scenario, you would parse 'full_text' using regex,
    # string manipulation, or more advanced ML models to extract the fields.
    # For example:
    lines = full_text.split('\n')
    for line in lines:
        if "TOTAL" in line.upper():
            try:
                # This is a very basic example; real parsing would be more robust
                total_amount = float(''.join(filter(str.isdigit or str.isalpha, line)).replace("TOTAL", "").strip())
            except ValueError:
                pass
        # More sophisticated parsing logic for merchant, tax, and items would go here.

    return {
        "merchant": merchant_name,
        "tax": tax_amount,
        "total": total_amount,
        "items": items,
        "raw_text": full_text
    }
