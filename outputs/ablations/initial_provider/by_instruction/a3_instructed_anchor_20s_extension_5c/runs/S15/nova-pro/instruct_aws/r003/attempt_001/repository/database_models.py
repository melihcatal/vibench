from typing import Dict

def normalize_item(item: Dict) -> Dict:
    return {k: {'S': str(v)} for k, v in item.items()}

def normalize_key(key: Dict) -> Dict:
    return {k: {'S': str(v)} for k, v in key.items()}

def normalize_expression_attribute_values(values: Dict) -> Dict:
    return {k: {'S': str(v)} for k, v in values.items()}