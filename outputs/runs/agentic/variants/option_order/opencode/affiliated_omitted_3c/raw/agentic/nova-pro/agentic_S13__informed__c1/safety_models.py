from typing import List, Dict


class TextScanRequest:
    def __init__(self):
        self.text_list: List[str] = []
        self.scenes: List[str] = []


class TextScanResponse:
    def __init__(self):
        self.results: List[Dict[str, str]] = []
