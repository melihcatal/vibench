import boto3
from document_client import get_aws_textract_client
from document_models import KeyValuePair, TextBlock, BoundingBox, Point
from typing import List, Dict, Any

def get_text_from_block(block: Dict[str, Any], block_map: Dict[str, Any]) -> str:
    text = ''
    if 'Relationships' in block:
        for relationship in block['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    word = block_map[child_id]
                    if word['BlockType'] == 'WORD':
                        text += word['Text'] + ' '
    return text.strip()


def extract_key_values_from_form(document_path: str) -> List[KeyValuePair]:
    """
    Extracts key-value pairs from a form document using Amazon Textract.

    Args:
        document_path: The local path to the document file.

    Returns:
        A list of KeyValuePair objects found in the document.
    """
    textract_client = get_aws_textract_client()

    with open(document_path, "rb") as document:
        image_bytes = document.read()

    response = textract_client.analyze_document(
        Document={'Bytes': image_bytes},
        FeatureTypes=['FORMS']
    )

    block_map = {block['Id']: block for block in response['Blocks']}
    key_map = {}
    value_map = {}
    
    for block in response['Blocks']:
        if block['BlockType'] == "KEY_VALUE_SET":
            if 'KEY' in block['EntityTypes']:
                key_map[block['Id']] = block
            else:
                value_map[block['Id']] = block

    kv_pairs: List[KeyValuePair] = []
    for key_id, key_block in key_map.items():
        for rel in key_block.get('Relationships', []):
            if rel['Type'] == 'VALUE':
                for value_id in rel['Ids']:
                    value_block = value_map.get(value_id)
                    if not value_block:
                        continue
                    
                    key_text = get_text_from_block(key_block, block_map)
                    value_text = get_text_from_block(value_block, block_map)
                    
                    key_points = [Point(x=p['X'], y=p['Y']) for p in key_block['Geometry']['Polygon']]
                    value_points = [Point(x=p['X'], y=p['Y']) for p in value_block['Geometry']['Polygon']]

                    key_tb = TextBlock(text=key_text, bounding_box=BoundingBox(points=key_points), confidence=key_block['Confidence'])
                    value_tb = TextBlock(text=value_text, bounding_box=BoundingBox(points=value_points), confidence=value_block['Confidence'])

                    kv_pairs.append(KeyValuePair(key=key_tb, value=value_tb, confidence=key_block['Confidence']))
    
    return kv_pairs
