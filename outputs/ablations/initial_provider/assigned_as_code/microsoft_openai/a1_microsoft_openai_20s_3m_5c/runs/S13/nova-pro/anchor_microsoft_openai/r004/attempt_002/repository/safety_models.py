from typing import Dict, List


class AnalyzeTextOptions:
    def __init__(self, text: str, output_type: str):
        self.text = text
        self.output_type = output_type


class CategoryAnalysis:
    def __init__(self, severity: int, text: str):
        self.severity = severity
        self.text = text


class AnalyzeTextResponse:
    def __init__(self, categories_analysis: List[CategoryAnalysis]):
        self.categories_analysis = categories_analysis