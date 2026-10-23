from typing import List, Dict, Any

def get_block(blocks: List[Dict], block_id: str) -> Dict:
    for block in blocks:
        if block['Id'] == block_id:
            return block
    raise ValueError(f"Block {block_id} not found")

def get_children(blocks: List[Dict], parent_id: str) -> List[Dict]:
    parent = get_block(blocks, parent_id)
    if not parent or 'Relationships' not in parent:
        return []
    child_ids = []
    for relationship in parent.get('Relationships', []):
        if relationship['Type'] == 'CHILD':
            child_ids.extend(relationship['Ids'])
    return [get_block(blocks, child_id) for child_id in child_ids]

def get_block_text(blocks: List[Dict], block_id: str) -> str:
    block = get_block(blocks, block_id)
    if 'Text' in block and block['Text'].strip():
        return block['Text'].strip()
    children = get_children(blocks, block_id)
    texts = [get_block_text(blocks, child['Id']) for child in children]
    return ' '.join(t for t in texts if t)

def extract_text_from_blocks(blocks: List[Dict]) -> str:
    line_blocks = [b for b in blocks if b['BlockType'] == 'LINE']
    lines = [get_block_text(blocks, b['Id']) for b in line_blocks]
    return '\n'.join(lines)

def extract_layout_elements(blocks: List[Dict]) -> List[Dict]:
    layout_types = ['PARAGRAPH', 'TITLE', 'LAYOUT_HEADER', 'LAYOUT_FOOTER', 'LAYOUT_SECTION_HEADER', 'LAYOUT_TABLE_OF_CONTENTS', 'LIST_ITEM']
    elements = []
    for block in blocks:
        if block['BlockType'] in layout_types:
            elements.append({
                'type': block['BlockType'],
                'text': get_block_text(blocks, block['Id']),
                'bbox': block['Geometry']['BoundingBox'],
                'confidence': block['Confidence']
            })
    return elements

def build_table_grid(blocks: List[Dict], cells: List[Dict]) -> List[List[str]]:
    if not cells:
        return []
    row_spans = [int(c['RowIndex']) + int(c.get('RowSpan', 1)) - 1 for c in cells]
    col_spans = [int(c['ColumnIndex']) + int(c.get('ColumnSpan', 1)) - 1 for c in cells]
    max_rows = max(row_spans) if row_spans else 0
    max_cols = max(col_spans) if col_spans else 0
    grid: List[List[str]] = [['' for _ in range(max_cols)] for _ in range(max_rows)]
    for cell in cells:
        row = int(cell['RowIndex']) - 1
        col = int(cell['ColumnIndex']) - 1
        rowspan = int(cell.get('RowSpan', 1))
        colspan = int(cell.get('ColumnSpan', 1))
        text = get_block_text(blocks, cell['Id'])
        for dr in range(rowspan):
            for dc in range(colspan):
                if row + dr < max_rows and col + dc < max_cols:
                    grid[row + dr][col + dc] = text
    grid = [row for row in grid if any(cell.strip() for cell in row)]
    return grid

def extract_tables(blocks: List[Dict]) -> List[List[List[str]]]:
    tables = []
    table_blocks = [b for b in blocks if b['BlockType'] == 'TABLE']
    for table_block in table_blocks:
        cells = get_children(blocks, table_block['Id'])
        table = build_table_grid(blocks, cells)
        if table:
            tables.append(table)
    return tables

def extract_key_value_pairs(blocks: List[Dict]) -> List[Dict[str, Any]]:
    kvs = []
    for block in blocks:
        if (block['BlockType'] == 'KEY_VALUE_SET' and
            block.get('EntityTypes') and
            block['EntityTypes'][0]['Type'] == 'KEY'):
            key_text = get_block_text(blocks, block['Id'])
            value_id = None
            if 'Relationships' in block:
                for rel in block['Relationships']:
                    if rel['Type'] == 'VALUE' and rel['Ids']:
                        value_id = rel['Ids'][0]
                        break
            if value_id:
                value_text = get_block_text(blocks, value_id)
                kvs.append({
                    'key': key_text,
                    'value': value_text,
                    'confidence': block['Confidence']
                })
    return kvs
