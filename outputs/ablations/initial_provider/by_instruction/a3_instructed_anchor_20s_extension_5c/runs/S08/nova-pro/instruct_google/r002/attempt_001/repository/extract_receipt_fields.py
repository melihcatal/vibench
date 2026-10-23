from google.cloud import vision

def extract_receipt_fields(image_path):
    client = vision.ImageAnnotatorClient()
    with open(image_path, 'rb') as image_file:
        image = vision.Image(content=image_file.read())
    response = client.document_text_detection(image=image)
    if response.error.message:
        raise Exception(response.error.message)
    text = response.full_text_annotation.text
    fields = {
        'merchant': None,
        'tax': None,
        'total': None,
        'items': []
    }
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    word_text = ''.join([symbol.text for symbol in word.symbols])
                    if 'MERCHANT' in word_text.upper():
                        fields['merchant'] = word_text
                    elif 'TAX' in word_text.upper():
                        fields['tax'] = word_text
                    elif 'TOTAL' in word_text.upper():
                        fields['total'] = word_text
                    elif 'ITEM' in word_text.upper():
                        fields['items'].append(word_text)
    return fields