from typing import Optional, List, Dict


class ModerationResult:
    def __init__(
        self,
        text: str,
        categories: Dict[str, float],
        overall_decision: str,
        flagged_spans: Optional[List[Dict]] = None,
    ):
        self.text = text
        self.categories = categories
        self.overall_decision = overall_decision
        self.flagged_spans = flagged_spans

    def to_dict(self):
        return {
            "text": self.text,
            "categories": self.categories,
            "overall_decision": self.overall_decision,
            "flagged_spans": self.flagged_spans,
        }


class BatchModerationRequest:
    def __init__(self, texts: List[str]):
        self.texts = texts


class BatchModerationResponse:
    def __init__(self, results: List[ModerationResult]):
        self.results = results

    def to_dict(self):
        return [result.to_dict() for result in self.results]
