
from google.cloud import vision
import os

def run_ocr_on_document(gcs_source_uri: str):
    """
    Runs OCR on a document stored in Google Cloud Storage using Google Cloud Vision API.

    Args:
        gcs_source_uri: The Google Cloud Storage URI of the document (e.g., "gs://your-bucket-name/path/to/document.pdf").

    Returns:
        A dictionary containing the detected text and any other relevant OCR results.
    """
    client = vision.ImageAnnotatorClient()

    # Supported file types for document text detection are PDF, TIFF, and GIF.
    # The `gcs_source_uri` can be a path to a PDF or TIFF file.
    image = vision.Image(source=vision.ImageSource(gcs_uri=gcs_source_uri))

    # Perform document text detection
    response = client.document_text_detection(image=image)
    
    # Extract text from the response
    full_text_annotation = response.full_text_annotation
    
    result = {
        "text": full_text_annotation.text,
        "pages": []
    }

    for page in full_text_annotation.pages:
        page_text = ""
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = "".join([symbol.text for symbol in word.symbols])
                    page_text += word_text + " "
        result["pages"].append({"page_number": page.page_number, "text": page_text.strip()})

    return result

