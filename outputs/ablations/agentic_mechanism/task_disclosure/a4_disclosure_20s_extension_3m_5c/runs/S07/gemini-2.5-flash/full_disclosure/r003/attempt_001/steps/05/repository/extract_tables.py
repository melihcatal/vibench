from google.cloud import vision
import io

def extract_tables_from_document(image_content: bytes):
    """
    Extracts table cells and row structure from a document image using Google Cloud Vision AI.

    Args:
        image_content: The content of the image file (e.g., PNG, JPEG) as bytes.

    Returns:
        A dictionary containing the extracted tables, their rows, and cells.
    """
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_content)

    response = client.document_text_detection(image=image)
    document = response.full_text_annotation

    tables_data = []

    # Helper to get text from a bounding box
    def get_text_from_bounding_box(bounds, document_pages):
        text = []
        for page in document_pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        for symbol in word.symbols:
                            if symbol.bounding_box.vertices[0].x >= bounds.vertices[0].x and \
                               symbol.bounding_box.vertices[0].y >= bounds.vertices[0].y and \
                               symbol.bounding_box.vertices[2].x <= bounds.vertices[2].x and \
                               symbol.bounding_box.vertices[2].y <= bounds.vertices[2].y:
                                text.append(symbol.text)
        return "".join(text)

    if document.pages:
        for page in document.pages:
            for block in page.blocks:
                if block.block_type == vision.Block.BlockType.TABLE:
                    table_info = {
                        "bounding_box": [(v.x, v.y) for v in block.bounding_box.vertices],
                        "rows": []
                    }
                    for paragraph in block.paragraphs:
                        # Assuming each paragraph within a table block might represent a row or part of a row
                        # This part might need more sophisticated logic for precise row/cell detection
                        # For simplicity, let's treat each paragraph as a potential row for now
                        row_text = "".join([word.text for word in paragraph.words])
                        if row_text:
                            table_info["rows"].append({"cells": [{"text": row_text, "bounding_box": [(v.x, v.y) for v in paragraph.bounding_box.vertices]}]})
                    tables_data.append(table_info)
    
    # More robust table extraction would typically involve parsing the `text_annotations`
    # and then correlating them with detected table bounding boxes.
    # The current Vision AI client might not directly give a structured table object
    # from document_text_detection, but rather individual text elements.
    # For a fully structured table, you might need to use `table_detection` if available,
    # or implement custom parsing logic based on text and bounding box locations.

    # This example focuses on demonstrating the use of Vision AI for document processing,
    # and provides a basic structure for table data, acknowledging that full table
    # structure parsing (rows, columns, merged cells) is complex and often
    # requires more advanced post-processing or a dedicated table extraction API.
    
    return {"tables": tables_data, "full_text": document.text_content}

