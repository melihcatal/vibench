from google.cloud import vision

def run_ocr_on_document(gcs_uri: str):
    """
    Runs OCR on a document stored in Google Cloud Storage.

    Args:
        gcs_uri: The Google Cloud Storage URI of the document (e.g., "gs://bucket-name/path/to/document.pdf").

    Returns:
        A dictionary containing the OCR results.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(source=vision.ImageSource(gcs_uri=gcs_uri))

    response = client.document_text_detection(image=image)
    
    # You can process the response further to extract specific information
    # For now, we'll return the full response as a dictionary (after converting to dict if needed)
    # The response object itself is a protobuf message, which can be directly used or converted.
    # For simplicity, returning the text content directly for demonstration.
    full_text_annotation = response.full_text_annotation
    
    return {
        "text": full_text_annotation.text,
        "pages": [
            {
                "page_number": i + 1,
                "width": page.width,
                "height": page.height,
                "blocks": [
                    {
                        "block_type": block.block_type.name,
                        "text": "".join([symbol.text for paragraph in block.paragraphs for word in paragraph.words for symbol in word.symbols]),
                        "bounding_box": [(v.x, v.y) for v in block.bounding_box.vertices]
                    } for block in page.blocks
                ]
            } for i, page in enumerate(response.full_text_annotation.pages)
        ]
    }
