from google.cloud import vision
from typing import List, Dict, Any
from document_models import DocumentInput, ExtractedLayout

def extract_layout_from_document(document_input: DocumentInput) -> ExtractedLayout:
    """Extracts blocks, lines, and other layout elements from a document using Google Cloud Vision API.

    This function uses DOCUMENT_TEXT_DETECTION to get more granular layout information.
    """
    client = vision.ImageAnnotatorClient()

    with open(document_input.image_path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    layout_data = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            block_info = {
                "bounding_box": [ (v.x, v.y) for v in block.bounding_box.vertices ],
                "paragraphs": []
            }
            for paragraph in block.paragraphs:
                paragraph_info = {
                    "bounding_box": [ (v.x, v.y) for v in paragraph.bounding_box.vertices ],
                    "words": []
                }
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    paragraph_info["words"].append({
                        "text": word_text,
                        "bounding_box": [ (v.x, v.y) for v in word.bounding_box.vertices ]
                    })
                block_info["paragraphs"].append(paragraph_info)
            layout_data.append(block_info)
    
    return ExtractedLayout(layout_data=layout_data)

if __name__ == "__main__":
    # Example usage: Replace with a valid image path
    # document_input = DocumentInput(image_path="path/to/your/document.png")
    # layout = extract_layout_from_document(document_input)
    # print(layout.layout_data)
    pass
