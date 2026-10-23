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
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    if 'Vendor' in word_text:
                        vendor = word_text.split(':')[1].strip()
                    elif 'Date' in word_text:
                        date = word_text.split(':')[1].strip()
                    elif 'Total' in word_text:
                        total = word_text.split(':')[1].strip()
                    elif 'Item' in word_text:
                        line_items.append(word_text.split(':')[1].strip())
    return {'vendor': vendor, 'date': date, 'total': total, 'line_items': line_items}