from typing import TypedDict, Dict, List, Any

SafetyResult = TypedDict(
    "SafetyResult",
    {
        "categories": Dict[str, float],
        "overall_blocked": bool,
        "rationale": str,
        "redacted_text": str,
        "flagged_spans": List[Dict[str, Any]],
        "raw_response": Dict[str, Any],
    },
    total=False,
)
