from google.cloud import vision

def extract_layout(image_content: bytes):
    """
    Extracts blocks, lines, and tables from a document image using Google Cloud Vision AI.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.document_text_detection(image=image)
    
    # You can customize the extraction to focus on specific elements like blocks, paragraphs, or tables.
    # For a more comprehensive layout analysis, consider using the Document Understanding AI.

    # Example: Extracting blocks and lines
    blocks = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            block_info = {
                "bounding_box": [(v.x, v.y) for v in block.bounding_box.vertices],
                "confidence": block.confidence,
                "paragraphs": []
            }
            for paragraph in block.paragraphs:
                paragraph_info = {
                    "bounding_box": [(v.x, v.y) for v in paragraph.bounding_box.vertices],
                    "confidence": paragraph.confidence,
                    "words": []
                }
                for word in paragraph.words:
                    word_text = "".join([symbol.text for symbol in word.symbols])
                    paragraph_info["words"].append({
                        "text": word_text,
                        "bounding_box": [(v.x, v.y) for v in word.bounding_box.vertices],
                        "confidence": word.confidence
                    })
                block_info["paragraphs"].append(paragraph_info)
            blocks.append(block_info)

    return {"blocks": blocks, "full_text": response.full_text_annotation.text}
