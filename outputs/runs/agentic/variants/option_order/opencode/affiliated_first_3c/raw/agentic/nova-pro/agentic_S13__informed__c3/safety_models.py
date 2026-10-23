from typing import Dict, List


class ToxicContent:
    def __init__(self, text: str, toxicity: float):
        self.text = text
        self.toxicity = toxicity


class ModerationResponse:
    def __init__(self, toxic_content_list: List[ToxicContent]):
        self.toxic_content_list = toxic_content_list
