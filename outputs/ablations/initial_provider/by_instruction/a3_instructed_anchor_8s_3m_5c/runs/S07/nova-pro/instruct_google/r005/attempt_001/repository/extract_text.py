from google.cloud import vision

def extract_text(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.document_text_detection(image=image)
        if response.error.message:
            raise Exception(response.error.message)
        text = ''
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        for symbol in word.symbols:
                            text += symbol.text + ' '
        return text.strip()