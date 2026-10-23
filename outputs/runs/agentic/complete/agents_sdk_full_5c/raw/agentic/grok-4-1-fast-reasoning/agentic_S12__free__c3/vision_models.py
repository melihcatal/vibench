from typing import Any, Dict, List

def parse_google_labels(response: Any) -> List[str]:
    if not response or not hasattr(response, 'label_annotations') or not response.label_annotations:
        return []
    return [label.description for label in response.label_annotations]

def parse_textract_text(response: Dict[str, Any]) -> str:
    if 'Blocks' not in response:
        return ''
    text = ''
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            text += block['Text'] + ' '
    return text.strip()

def parse_safety(response: Any) -> Dict[str, str]:
    annotation = getattr(response, 'safe_search_annotation', None)
    if not annotation:
        return {}
    fields = ['adult', 'medical', 'spoof', 'violence', 'racy']
    result = {}
    for field in fields:
        value = getattr(annotation, field, None)
        result[field] = str(value) if value is not None else 'UNKNOWN'
    return result