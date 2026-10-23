from typing import Dict


def normalize_text_response(response: Dict) -> str:
    return response['text']


def normalize_layout_response(response: Dict) -> Dict:
    return response['layout']


def normalize_tables_response(response: Dict) -> Dict:
    return response['tables']


def normalize_key_values_response(response: Dict) -> Dict:
    return response['key_values']