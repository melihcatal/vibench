import os
import re
from google.cloud import vision

def extract_receipt_fields(image_path):
    """
    Extracts merchant, tax, total, and items from a receipt image using Google Cloud Vision AI.
    """
    client = vision.ImageAnnotatorClient()

    with open(image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    merchant = "Unknown Merchant"
    total = None
    tax = None
    items = []

    # Extracting merchant (simplistic, often found in the first few lines or dominant text)
    if document.pages:
        for page in document.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        word_text = "".join([symbol.text for symbol in word.symbols])
                        # A very basic heuristic for merchant name
                        if len(word_text) > 3 and word.bounding_box.vertices[0].y < 200: # Assuming merchant is near the top
                            if merchant == "Unknown Merchant": # Only take the first likely candidate
                                merchant = word_text
                            break
                    if merchant != "Unknown Merchant":
                        break
                if merchant != "Unknown Merchant":
                    break

    # Extracting total, tax, and items from the full text
    full_text = document.text
    lines = full_text.split('\\n')

    for line in lines:
        line = line.strip()

        # Try to find total (example: "TOTAL 123.45" or "AMOUNT DUE 123.45")
        total_match = re.search(r'(TOTAL|AMOUNT DUE|BALANCE)\s*[\$£€]?\s*(\d+\.\d{2})', line, re.IGNORECASE)
        if total_match:
            total = float(total_match.group(2))

        # Try to find tax (example: "TAX 12.34" or "VAT 12.34")
        tax_match = re.search(r'(TAX|VAT|SALES TAX)\s*[\$£€]?\s*(\d+\.\d{2})', line, re.IGNORECASE)
        if tax_match:
            tax = float(tax_match.group(2))

        # Basic item extraction (lines that don't look like total/tax/date/address but contain text and maybe a price)
        # This is a very simplified heuristic and would need significant refinement for real-world use.
        if not total_match and not tax_match and \
           not re.search(r'^\d{1,2}/\d{1,2}/\d{2,4}', line) and \
           not re.search(r'^\s*\d+\s+X\s+\d+\.\d{2}', line) and \
           re.search(r'[a-zA-Z]{3,}', line) and \
           re.search(r'\d+\.\d{2}', line):
            items.append(line)

    return {
        "merchant": merchant,
        "tax": tax,
        "total": total,
        "items": items
    }

if __name__ == "__main__":
    # This is a placeholder for your receipt image path.
    # Replace with the actual path to your receipt image.
    # For this to work, you need to set up Google Cloud credentials.
    # For example, by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
    image_file_path = "path/to/your/receipt.jpg"

    if os.path.exists(image_file_path):
        extracted_data = extract_receipt_fields(image_file_path)
        print("Extracted Receipt Fields:")
        print(f"Merchant: {extracted_data['merchant']}")
        print(f"Tax: {extracted_data['tax']}")
        print(f"Total: {extracted_data['total']}")
        print("Items:")
        for item in extracted_data['items']:
            print(f"- {item}")
    else:
        print(f"Error: Image file not found at {image_file_path}")
        print("Please replace 'path/to/your/receipt.jpg' with the actual path to your receipt image.")
        print("Also, ensure you have Google Cloud Vision API enabled and credentials configured.")
