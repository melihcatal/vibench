from google.cloud import vision

def extract_document_layout(image_content: bytes):
    """
    Extracts blocks, lines, and other layout elements from a document image.

    Args:
        image_content: The content of the image file as bytes.

    Returns:
        A dictionary containing extracted layout elements, including pages, blocks, and paragraphs.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    features = [
        vision.Feature(type_=vision.Feature.Type.DOCUMENT_TEXT_DETECTION)
    ]

    response = client.annotate_image(image=image, features=features)

    # The full_text_annotation contains detailed layout information
    full_text_annotation = response.full_text_annotation
    
    # You can process full_text_annotation to extract blocks, paragraphs, words, etc.
    # For simplicity, this example returns a structured representation of pages, blocks, and paragraphs.
    
    extracted_layout = {
        "text": full_text_annotation.text,
        "pages": []
    }

    for page in full_text_annotation.pages:
        page_layout = {
            "page_number": page.page_number,
            "width": page.width,
            "height": page.height,
            "blocks": []
        }
        for block in page.blocks:
            block_layout = {
                "confidence": block.confidence,
                "bounding_box": [(v.x, v.y) for v in block.bounding_box.vertices],
                "paragraphs": []
            }
            for paragraph in block.paragraphs:
                paragraph_text = "".join([
                    symbol.text for word in paragraph.words for symbol in word.symbols
                ])
                paragraph_layout = {
                    "confidence": paragraph.confidence,
                    "bounding_box": [(v.x, v.y) for v in paragraph.bounding_box.vertices],
                    "text": paragraph_text
                }
                block_layout["paragraphs"].append(paragraph_layout)
            page_layout["blocks"].append(block_layout)
        extracted_layout["pages"].append(page_layout)

    return extracted_layout
