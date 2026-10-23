from google.cloud import vision

def extract_invoice_fields(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
    response = client.document_text_detection(image=image)
    if response.error.message:
        raise Exception(response.error.message)
    texts = response.full_text_annotation.text
    vendor = ''
    date = ''
    total = ''
    line_items = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            if 'VENDOR' in block.text:
                vendor = block.text
            elif 'DATE' in block.text:
                date = block.text
            elif 'TOTAL' in block.text:
                total = block.text
            elif 'ITEM' in block.text:
                line_items.append(block.text)
    return {'vendor': vendor, 'date': date, 'total': total, 'line_items': line_items}