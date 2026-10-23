import boto3
from document_client import get_textract_client
from document_models import ExtractedKeyValuePair
from typing import List, Dict, Any

def extract_key_values(image_bytes: bytes) -> List[ExtractedKeyValuePair]:
    """
    Extracts key-value pairs from a form-like document using AWS Textract.
    """
    textract_client = get_textract_client()
    response = textract_client.analyze_document(
        Document={'Bytes': image_bytes},
        Features=['FORMS']
    )

    key_value_pairs: List[ExtractedKeyValuePair] = []
    blocks = response.get('Blocks', [])
    
    # Helper to find text for a block ID
    block_map = {block['Id']: block for block in blocks}

    def get_text_from_ids(ids: List[str]) -> str:
        text = ""
        for id in ids:
            block = block_map.get(id)
            if block and block['BlockType'] == 'WORD':
                text += block.get('Text', '') + " "
        return text.strip()

    for block in blocks:
        if block['BlockType'] == 'KEY_VALUE_SET' and 'KEY' in block['EntityTypes']:
            key_text = ""
            value_text = ""
            key_geometry = None
            value_geometry = None
            confidence = block.get('Confidence')

            for relationship in block.get('Relationships', []):
                if relationship['Type'] == 'CHILD':
                    key_text = get_text_from_ids(relationship['Ids'])
                    key_block_id = relationship['Ids'][0] if relationship['Ids'] else None
                    if key_block_id and block_map.get(key_block_id):
                        key_geometry = block_map.get(key_block_id).get('Geometry')

                elif relationship['Type'] == 'VALUE':
                    for value_id in relationship['Ids']:
                        value_block = block_map.get(value_id)
                        if value_block and 'VALUE' in value_block['EntityTypes']:
                            for value_relationship in value_block.get('Relationships', []):
                                if value_relationship['Type'] == 'CHILD':
                                    value_text = get_text_from_ids(value_relationship['Ids'])
                                    value_geometry = value_block.get('Geometry')
                                    break # Assuming one value per key
                    
            if key_text or value_text:
                key_value_pairs.append(ExtractedKeyValuePair(
                    key=key_text,
                    value=value_text,
                    key_geometry=key_geometry,
                    value_geometry=value_geometry,
                    confidence=confidence
                ))

    return key_value_pairs
