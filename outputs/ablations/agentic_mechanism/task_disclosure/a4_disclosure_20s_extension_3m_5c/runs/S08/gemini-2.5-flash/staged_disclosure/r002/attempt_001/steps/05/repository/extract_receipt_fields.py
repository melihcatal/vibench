from google.cloud import vision
import os

def extract_receipt_fields(image_path):
    """
    Extracts merchant, tax, total, and items from a receipt image using Google Cloud Vision API.
    """
    # Set up Google Cloud Vision client
    client = vision.ImageAnnotatorClient()

    # Read the image file
    with open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    # Perform text detection
    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    merchant = "N/A"
    tax = "N/A"
    total = "N/A"
    items = []

    # Simple parsing logic (can be enhanced for better accuracy)
    # This is a basic example and might need more sophisticated NLP for real-world scenarios
    lines = document.text.split('\n')
    for line in lines:
        line_lower = line.lower()
        if "merchant" in line_lower and merchant == "N/A":
            # This is a placeholder; actual merchant extraction would be more complex
            merchant = line.strip() 
        elif "tax" in line_lower and tax == "N/A":
            try:
                tax = "".join(filter(str.isdigit or str.isdecimal, line_lower.split("tax")[-1].strip().replace("$","")))
            except ValueError:
                pass
        elif ("total" in line_lower or "amount" in line_lower) and total == "N/A":
            try:
                total = "".join(filter(str.isdigit or str.isdecimal, line_lower.split("total")[-1].strip().replace("$","")))
            except ValueError:
                pass
        else:
            # Example for items: lines with a possible quantity and price
            # This is highly simplified
            words = line.split()
            if len(words) > 1 and any(word.replace('.', '', 1).isdigit() for word in words):
                items.append(line.strip())

    # Further refinement for merchant, tax, and total could involve regex and positional analysis
    # For a real application, consider using a more robust receipt parsing library or service if available.

    return {
        "merchant": merchant,
        "tax": tax,
        "total": total,
        "items": items
    }

if __name__ == '__main__':
    # Example usage:
    # Ensure you have authenticated to Google Cloud and set up your project.
    # For example, by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"

    # Create a dummy image file for testing (in a real scenario, this would be a receipt image)
    dummy_image_content = b"This is a dummy image content."
    dummy_image_path = "dummy_receipt.jpg"
    with open(dummy_image_path, "wb") as f:
        f.write(dummy_image_content)

    # In a real scenario, replace "dummy_receipt.jpg" with the path to your actual receipt image
    # For this example, we'll just run it with the dummy file, which will likely not extract meaningful data.
    # The purpose is to demonstrate the structure and provider integration.
    extracted_data = extract_receipt_fields(dummy_image_path)
    print(f"Extracted Data: {extracted_data}")

    # Clean up the dummy image file
    os.remove(dummy_image_path)
