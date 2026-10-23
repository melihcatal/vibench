import base64
from typing import List
from document_client import get_textract_client
from document_models import KeyValue

def extract_key_values_from_image(image_bytes: bytes) -> List[KeyValue]:
    textract_client = get_textract_client()
    response = textract_client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['FORMS']
    )

    key_values = []
    blocks = response.get('Blocks', [])

    for block in blocks:
        if block['BlockType'] == 'KEY_VALUE_SET':
            if 'EntityType' in block and block['EntityType'] == 'KEY':
                key_text = "".join([b['Text'] for b in blocks if 'Id' in b and b['BlockType'] == 'WORD' and b['Id'] in block.get('Relationships', [])[0].get('Ids', [])]) if block.get('Relationships') else ''
                value_block_id = None
                for relationship in block.get('Relationships', []):
                    if relationship['Type'] == 'VALUE':
                        if relationship['Ids']:
                            value_block_id = relationship['Ids'][0]
                            break
                
                if value_block_id:
                    value_block = next((b for b in blocks if b['Id'] == value_block_id and b['BlockType'] == 'KEY_VALUE_SET'), None)
                    if value_block and 'EntityType' in value_block and value_block['EntityType'] == 'VALUE':
                        value_text = "".join([b['Text'] for b in blocks if 'Id' in b and b['BlockType'] == 'WORD' and b['Id'] in value_block.get('Relationships', [])[0].get('Ids', [])]) if value_block.get('Relationships') else ''
                        key_values.append(KeyValue(
                            key=key_text,
                            value=value_text,
                            confidence=block['Confidence'] # Using key block's confidence
                        ))
    return key_values
