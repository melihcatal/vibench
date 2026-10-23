import os
import openai
from typing import List, Dict, Any

class SafetyCheckResult:
    def __init__(self, text: str, flagged: bool, categories: Dict[str, bool], category_scores: Dict[str, float]):
        self.text = text
        self.flagged = flagged
        self.categories = categories
        self.category_scores = category_scores

def check_corpus_safety(texts: List[str]) -> List[SafetyCheckResult]:
    client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    results = []
    for text in texts:
        response = client.moderations.create(input=text)
        moderation_output = response.results[0]
        results.append(SafetyCheckResult(
            text=text,
            flagged=moderation_output.flagged,
            categories=moderation_output.categories.model_dump(),
            category_scores=moderation_output.category_scores.model_dump()
        ))
    return results
