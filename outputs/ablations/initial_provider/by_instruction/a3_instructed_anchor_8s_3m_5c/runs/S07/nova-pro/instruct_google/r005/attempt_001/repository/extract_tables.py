from google.cloud import vision

def extract_tables(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
        response = client.document_text_detection(image=image)
        if response.error.message:
            raise Exception(response.error.message)
        tables = []
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                if block.block_type == vision.Document.Block.Table:
                    tables.append({'bounding_box': block.bounding_box, 'text': block.text})
        return tables