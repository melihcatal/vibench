from typing import List, Dict, Any

def extract_plain_text(blocks: List[Dict[str, Any]]) -> str:
    lines = [block['Text'] for block in blocks if block['BlockType'] == 'LINE']
    return '\n'.join(lines)

def extract_layout(blocks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    layout_elements = []
    for block in blocks:
        if block['BlockType'] in ['WORD', 'LINE', 'PARAGRAPH', 'LAYOUT_HEADER', 'LAYOUT_FOOTER', 'LAYOUT_TITLE', 'LAYOUT_TABLE']:
            element = {
                'id': block['Id'],
                'type': block['BlockType'],
                'text': block.get('Text', ''),
                'confidence': block.get('Confidence', 0.0),
                'geometry': block['Geometry']
            }
            layout_elements.append(element)
    return layout_elements

def extract_tables(blocks: List[Dict[str, Any]]) -> List[List[List[str]]]:
    tables = []
    cells_by_id: Dict[str, Dict[str, Any]] = {b['Id']: b for b in blocks}
    for block in blocks:
        if block['BlockType'] != 'TABLE':
            continue
        child_rels = [r for r in block.get('Relationships', []) if r['Type'] == 'CHILD']
        child_ids = [cid for rel in child_rels for cid in rel['Ids']]
        cell_blocks = [cells_by_id.get(cid) for cid in child_ids if cells_by_id.get(cid, {}).get('BlockType') == 'CELL']
        if not cell_blocks:
            continue
        row_indices = [int(c['RowIndex']) for c in cell_blocks]
        col_indices = [int(c['ColumnIndex']) for c in cell_blocks]
        max_rows = max(row_indices) + 1 if row_indices else 0
        max_cols = max(col_indices) + 1 if col_indices else 0
        if max_rows == 0 or max_cols == 0:
            continue
        table: List[List[str]] = [['' for _ in range(max_cols)] for _ in range(max_rows)]
        for cell in cell_blocks:
            row = int(cell['RowIndex'])
            col = int(cell['ColumnIndex'])
            rowspan = int(cell.get('RowSpan', 1))
            colspan = int(cell.get('ColumnSpan', 1))
            cell_text = cell['Text'].strip()
            for dr in range(rowspan):
                for dc in range(colspan):
                    tr = row + dr
                    tc = col + dc
                    if tr < max_rows and tc < max_cols:
                        if table[tr][tc] == '':
                            table[tr][tc] = cell_text
                        else:
                            table[tr][tc] += ' ' + cell_text
        tables.append(table)
    return tables

def extract_key_values(blocks: List[Dict[str, Any]]) -> Dict[str, str]:
    key_map: Dict[str, str] = {}
    value_map: Dict[str, str] = {}
    for block in blocks:
        if block['BlockType'] == 'KEY':
            key_map[block['Id']] = block['Text'].strip()
        elif block['BlockType'] == 'VALUE':
            value_map[block['Id']] = block['Text'].strip()
    kv_pairs: Dict[str, str] = {}
    for block in blocks:
        if block['BlockType'] == 'KEY' and 'Relationships' in block:
            for rel in block['Relationships']:
                if rel['Type'] == 'VALUE':
                    for value_id in rel['Ids']:
                        value_text = value_map.get(value_id)
                        if value_text:
                            kv_pairs[key_map[block['Id']]] = value_text
                            break
    return kv_pairs
