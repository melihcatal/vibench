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
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    if 'Merchant' in word_text:
                        merchant = word_text.split(':')[1].strip()
                    elif 'Tax' in word_text:
                        tax = word_text.split(':')[1].strip()
                    elif 'Total' in word_text:
                        total = word_text.split(':')[1].strip()
                    elif 'Item' in word_text:
                        items.append(word_text.split(':')[1].strip())
    return {'merchant': merchant, 'tax': tax, 'total': total, 'items': items}