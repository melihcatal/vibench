from typing import List, Dict, Any, Tuple

def extract_plain_text(response: dict) -> str:
    blocks: List[Dict[str, Any]] = response.get('Blocks', [])
    lines = [block['Text'] for block in blocks if block['BlockType'] == 'LINE']
    return '\\n'.join(lines)

def extract_layout_elements(response: dict) -> List[Dict[str, Any]]:
    blocks: List[Dict[str, Any]] = response.get('Blocks', [])
    layout = []
    for block in blocks:
        block_type = block['BlockType']
        if block_type not in ['WORD', 'SELECTION_ELEMENT']:
            layout.append({
                'type': block_type,
                'text': block.get('Text', ''),
                'confidence': block.get('Confidence', 0.0),
                'geometry': block.get('Geometry', {}),
            })
    return layout

def extract_tables(response: dict) -> List[List[List[str]]]:
    blocks: List[Dict[str, Any]] = response.get('Blocks', [])
    tables = []
    table_blocks = [b for b in blocks if b['BlockType'] == 'TABLE']
    for table_block in table_blocks:
        cells: Dict[Tuple[int, int], str] = {}
        for relationship in table_block.get('Relationships', []):
            if relationship['Type'] == 'CHILD':
                for child_id in relationship['Ids']:
                    cell_block = next((b for b in blocks if b['Id'] == child_id), None)
                    if cell_block and cell_block['BlockType'] == 'CELL':
                        row = cell_block['RowIndex']
                        col = cell_block['ColumnIndex']
                        cells[(row, col)] = cell_block.get('Text', '') or ''
        if cells:
            max_row = max(r for r, _ in cells)
            max_col = max(c for _, c in cells)
            table_grid: List[List[str]] = [['' for _ in range(max_col + 1)] for _ in range(max_row + 1)]
            for (r, c), text in cells.items():
                table_grid[r][c] = text
            tables.append(table_grid)
    return tables

def extract_key_value_pairs(response: dict) -> Dict[str, str]:
    blocks: List[Dict[str, Any]] = response.get('Blocks', [])
    keys: Dict[str, Dict[str, Any]] = {}
    values: Dict[str, Dict[str, Any]] = {}
    for block in blocks:
        if block['BlockType'] == 'KEY_VALUE_SET':
            entity_types = [et['Type'] for et in block.get('EntityTypes', [])]
            block_id = block['Id']
            geo = block['Geometry']
            if 'KEY' in entity_types:
                keys[block_id] = {'text': block['Text'], 'geometry': geo}
            elif 'VALUE' in entity_types:
                values[block_id] = {'text': block['Text'], 'geometry': geo}
    
    def y_center(geometry: Dict[str, Any]) -> float:
        bb = geometry['BoundingBox']
        return bb['Top'] + bb['Height'] / 2
    
    sorted_keys = sorted(keys.items(), key=lambda kv: y_center(kv[1]['geometry']))
    sorted_values = sorted(values.items(), key=lambda kv: y_center(kv[1]['geometry']))
    
    kv_pairs: Dict[str, str] = {}
    for (k_id, k_info), (v_id, v_info) in zip(sorted_keys, sorted_values):
        kv_pairs[k_info['text']] = v_info['text']
    
    return kv_pairs
