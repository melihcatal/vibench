import os
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.core.credentials import AzureKeyCredential
from document_client import get_document_client


def extract_text_from_image(image_path: str) -> str:
    """Extract plain text from a scanned document image using Azure Document Intelligence."""
    client = get_document_client()

    with open(image_path, "rb") as f:
        image_data = f.read()

    poller = client.begin_analyze_document(
        model_id="prebuilt-read",
        body=image_data,
        content_type="application/octet-stream",
    )

    result = poller.result()

    extracted_text = ""
    for page in result.pages:
        for line in page.lines:
            extracted_text += line.content + "\n"

    return extracted_text.strip()


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python extract_text.py <image_path>")
        sys.exit(1)

    text = extract_text_from_image(sys.argv[1])
    print(text)
