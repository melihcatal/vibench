from google.cloud import vision

def extract_layout(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.document_text_detection(image=image)
        if response.error.message:
            raise Exception(response.error.message)
        layout = []
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                layout.append({'bounding_box': block.bounding_box, 'text': block.text})
        return layout