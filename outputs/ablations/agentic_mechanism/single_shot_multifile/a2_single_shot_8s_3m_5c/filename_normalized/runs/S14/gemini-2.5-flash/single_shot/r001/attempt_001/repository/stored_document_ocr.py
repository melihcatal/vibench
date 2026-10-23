import os
from typing import List
from storage_client import get_textract_client
from storage_models import DocumentTextResponse

def run_ocr_on_stored_document(bucket_name: str, object_key: str) -> DocumentTextResponse:
    textract_client = get_textract_client()
    response = textract_client.analyze_document(
        Document={
            'S3Object': {
                'Bucket': bucket_name,
                'Name': object_key
            }
        },
        FeatureTypes=["FORMS", "TABLES"]
    )

    full_text = []
    detected_languages = set()

    for block in response['Blocks']:
        if block['BlockType'] == 'WORD':
            full_text.append(block['Text'])
        if block['BlockType'] == 'PAGE' and 'DetectedLanguages' in block:
            for lang_info in block['DetectedLanguages']:
                detected_languages.add(lang_info['LanguageCode'])

    return DocumentTextResponse(
        text_content=" ".join(full_text),
        detected_languages=list(detected_languages)
    )
