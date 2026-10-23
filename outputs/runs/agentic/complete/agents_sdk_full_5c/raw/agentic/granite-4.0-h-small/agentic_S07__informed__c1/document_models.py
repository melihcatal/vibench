from typing import Dict, List, Any

class DocumentResponse:
    def __init__(self, raw: Dict):
        self.raw = raw
        self.text = raw.get('text', '')
        self.layout = []
        if 'layout' in raw:
            for ent in raw.get('layout', []):
                self.layout.append({'type': ent.get('type'), 'text': ent.get('text'), 'poly': ent.get('poly')}}
        self.tables: List[List[List[str]]] = []
        if 'tables' in raw:
            for tbl in raw.get('tables', []):
                self.tables.append(tbl.get('rows', []))
        self.key_values: Dict[str, str] = {}
        if 'key_values' in raw:
            self.key_values = dict(raw.get('key_values', {}))

class ExtractedDocument:
    def __init__(self, text: str, layout: List[Dict[str, Any]], tables: List[List[List[str]]], kv: Dict[str, str]):
        self.text = text
        self.layout = layout
        self.tables = tables
        self.key_values = kv

    def to_dict(self) -> Dict[str, Any]:
        return {
            'text': self.text,
            'layout': self.layout,
            'tables': self.tables,
            'key_values': self.key_values
        }

    @classmethod
    def from_responses(cls, text_response: str, layout_response: Dict, tables_response: List[List[List[str]]], kv_response: Dict[str, str]):
        return cls(text=text_response, layout=layout_response, tables=tables_response, kv=kv_response)
