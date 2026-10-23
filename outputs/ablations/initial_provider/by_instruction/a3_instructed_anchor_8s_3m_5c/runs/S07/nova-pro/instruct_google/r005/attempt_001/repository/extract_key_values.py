from google.cloud import vision

def extract_key_values(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.document_text_detection(image=image)
        if response.error.message:
            raise Exception(response.error.message)
        key_values = {}
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        if word.property.detected_break.type == vision.TextAnnotation.DetectedBreak.BreakType.SPACE:
                            key_values[word.text] = ''
                        else:
                            key_values[word.text] = word.text
        return key_values