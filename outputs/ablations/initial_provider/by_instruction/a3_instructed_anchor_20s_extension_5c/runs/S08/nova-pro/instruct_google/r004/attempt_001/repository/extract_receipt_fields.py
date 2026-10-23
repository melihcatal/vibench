from google.cloud import vision

def extract_receipt_fields(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
    response = client.document_text_detection(image=image)
    if response.error.message:
        raise Exception(response.error.message)
    texts = response.full_text_annotation.text
    merchant = ''
    tax = ''
    total = ''
    items = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            if 'MERCHANT' in block.text:
                merchant = block.text
            elif 'TAX' in block.text:
                tax = block.text
            elif 'TOTAL' in block.text:
                total = block.text
            elif 'ITEM' in block.text:
                items.append(block.text)
    return {'merchant': merchant, 'tax': tax, 'total': total, 'items': items}