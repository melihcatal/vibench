from typing import Dict, List

class SafetyRequest:
    def __init__(self, text: str):
        self.text = text

    def to_dict(self):
        return {'input': self.text}

class SafetyResponse:
    def __init__(self, data: Dict):
        self.data = data

    def is_safe(self) -> bool:
        return self.data.get('safety', {}).get('is_safe', False)

    def get_unsafe_spans(self) -> List[Dict]:
        return self.data.get('safety', {}).get('unsafe_spans', [])