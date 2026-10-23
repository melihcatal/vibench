import os
from google.cloud import documentai

def extract_receipt_fields(file_path):
    client = documentai.DocumentProcessorServiceClient()
    project_id = os.environ['GOOGLE_CLOUD_PROJECT']
    location = 'us'
    processor_id = 'b1a8221621204655'
    processor = f'projects/{project_id}/locations/{location}/processors/{processor_id}'

    with open(file_path, 'rb') as image:
        image_content = image.read()

    document = {'content': image_content,'mime_type': 'application/pdf'}
    request = {'name': processor, 'document': document}

    result = client.process_document(request=request)
    document = result.document

    fields = {}
    for entity in document.entities:
        if entity.type_ == 'MERCHANT':
            fields['merchant'] = entity.mention_text
        elif entity.type_ == 'TAX':
            fields['tax'] = entity.mention_text
        elif entity.type_ == 'TOTAL':
            fields['total'] = entity.mention_text
        elif entity.type_ == 'ITEM':
            if 'items' not in fields:
                fields['items'] = []
            fields['items'].append(entity.mention_text)
    return fields