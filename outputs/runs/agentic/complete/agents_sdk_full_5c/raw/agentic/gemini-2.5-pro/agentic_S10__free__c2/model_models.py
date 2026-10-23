from typing import List, Dict, Any

# This file can be used to define shared data models for request and response
# payloads, helping with type checking and standardization across the application.

class SummarizeResponse:
    def __init__(self, summary: str, meta: Dict[str, Any]):
        self.summary = summary
        self.meta = meta

class JSONExtractionResponse:
    def __init__(self, data: Dict[str, Any], raw_text: str):
        self.data = data
        self.raw_text = raw_text

class QAContext:
    def __init__(self, documents: List[Dict[str, str]]):
        # Expects documents in the format Cohere's API uses: [{"text": "content"}, ...]
        self.documents = documents

class SafetyAssessment:
    def __init__(self, scores: Dict[str, float]):
        self.scores = scores
        self.is_safe = all(score < 0.7 for score in scores.values())
