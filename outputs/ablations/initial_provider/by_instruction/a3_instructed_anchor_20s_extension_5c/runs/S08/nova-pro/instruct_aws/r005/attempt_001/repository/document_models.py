from typing import Dict

def create_document_request(document: bytes) -> Dict:
    return {'Document': {'Bytes': document}, 'FeatureTypes': ['FORMS']}

def parse_document_response(response: Dict) -> Dict:
    extracted_data = {}
    for block in response['Blocks']:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'KEY' in block['Text']:
                extracted_data[block['KEY']['Text']] = block['VALUE']['Text']
    return extracted_data