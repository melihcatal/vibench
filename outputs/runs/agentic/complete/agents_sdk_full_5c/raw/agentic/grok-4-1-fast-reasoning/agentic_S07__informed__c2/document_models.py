from typing import List, Dict, Any, Tuple
import json

def _get_child_text(block_id: str, blocks: List[Dict[str, Any]]) -> str:
    block = next((b for b in blocks if b['Id'] == block_id), {})
    text = block.get('Text', '')
    if not text and 'Relationships' in block:
        for relationship in block['Relationships']:
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    text += ' ' + _get_child_text(child_id, blocks)
    return text.strip()

def normalize_ocr_text(blocks: List[Dict[str, Any]]) -> str:
    text_lines = []
    for block in blocks:
        if block['BlockType'] == 'LINE':
            text_lines.append(block.get('Text', ''))
    return '\n'.join(text_lines)

def extract_layout_elements(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [block for block in blocks if block['BlockType'] != 'WORD']

def parse_tables(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    tables = []
    for block in blocks:
        if block['BlockType'] == 'TABLE':
            cells = []
            for relationship in block.get('Relationships', []):
                if relationship['Type'] == 'CHILD':
                    for cell_id in relationship['Ids']:
                        cell = next((b for b in blocks if b['Id'] == cell_id), {})
                        cell_text = _get_child_text(cell['Id'], blocks)
                        cells.append({
                            'id': cell['Id'],
                            'text': cell_text,
                            'confidence': cell.get('Confidence', 0.0),
                            'geometry': cell.get('Geometry', {})
                        })
            tables.append({
                'table_id': block['Id'],
                'confidence': block.get('Confidence', 0.0),
                'cells': cells
            })
    return tables

def extract_key_value_pairs(blocks: List[Dict[str, Any]]) -> List[Tuple[str, str]]:
    key_map: Dict[str, str] = {}
    value_map: Dict[str, str] = {}
    for block in blocks:
        if block['BlockType'] == 'KEY_VALUE_SET':
            entity_types = block.get('EntityTypes', [])
            if 'KEY' in entity_types:
                key_map[block['Id']] = _get_child_text(block['Id'], blocks)
            elif 'VALUE' in entity_types:
                value_map[block['Id']] = _get_child_text(block['Id'], blocks)
    pairs = []
    for block in blocks:
        if block['BlockType'] == 'KEY_VALUE_SET' and 'KEY' in block.get('EntityTypes', []):
            for relationship in block.get('Relationships', []):
                if relationship['Type'] == 'VALUE':
                    for value_id in relationship['Ids']:
                        if value_id in value_map:
                            key = key_map.get(block['Id'], '')
                            value = value_map[value_id]
                            pairs.append((key, value))
    return pairs