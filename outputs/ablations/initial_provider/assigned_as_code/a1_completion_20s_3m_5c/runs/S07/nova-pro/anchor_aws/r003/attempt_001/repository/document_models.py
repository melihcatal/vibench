from typing import Dict, List

def normalize_text(text: str) -> str:
    return text.strip()

def normalize_layout(layout: Dict) -> Dict:
    return {
        'blocks': [normalize_text(block) for block in layout['blocks']],
        'lines': [normalize_text(line) for line in layout['lines']],
        'tables': layout['tables']
    }

def normalize_tables(tables: List[Dict]) -> List[Dict]:
    return [{'cells': [normalize_text(cell) for cell in table['cells']], 'rows': [normalize_text(row) for row in table['rows']]} for table in tables]

def normalize_key_values(key_values: Dict) -> Dict:
    return {normalize_text(key): normalize_text(value) for key, value in key_values.items()}