from google.cloud import vision

def extract_key_values(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.document_text_detection(image=image)
        key_values = {}
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                if block.block_type == vision.TextAnnotation.DetectedLanguage.BlockType.TABLE:
                    for row in block.rows:
                        key_values[row.cells[0].text] = row.cells[1].text
        return key_values