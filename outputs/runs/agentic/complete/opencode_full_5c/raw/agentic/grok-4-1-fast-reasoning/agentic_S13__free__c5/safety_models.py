from typing import TypedDict, Dict, List, Optional


class ModerationResult(TypedDict):
    input_text: str
    flagged: bool
    categories: Dict[str, float]
    rationale: Optional[str]


class BatchModerationResults(TypedDict):
    results: List[ModerationResult]
