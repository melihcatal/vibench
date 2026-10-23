from typing import Dict, List


def normalize_text(text: str) -> str:
    return text.strip()


def normalize_layout(layout: Dict) -> Dict:
    normalized_layout = {}
    for key, value in layout.items():
        if key == 'lines':
            normalized_layout[key] = [normalize_text(line) for line in value]
        elif key == 'tables':
            normalized_layout[key] = [{
                'id': table['id'],
                'cells': [normalize_text(cell) for cell in table['cells']]
            } for table in value]
        elif key == 'key_values':
            normalized_layout[key] = {normalize_text(key): normalize_text(value) for key, value in value}
    return normalized_layout