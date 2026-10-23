import os
from google.cloud import vision

def check_unsafe_content(decrypted_text):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/google-cloud-credentials.json'
    client = vision.ImageAnnotatorClient()

    document = vision.Document()
    document.text = decrypted_text

    response = client.document_text_detection(document=document)

    if response.error.message:
        raise Exception(
            '{}
For more info on error messages, check: {}
'.format(
                response.error.message,
                'https://cloud.google.com/apis/design/errors'
            )
        )

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    if any(symbol.description in ['SEXUAL', 'VIOLENCE', 'PROFANITY'] for symbol in word.symbols):
                        return True
    return False
