# Summarize moderation decisions
from typing import List, Dict
import pandas as pd
from safety_models import SafetyDecision, SafetyCategory


def summarize_moderation(decisions: List[SafetyDecision]) -> Dict[str, float]:
    """Summarize moderation decisions using pandas."""
    data = []
    for decision in decisions:
        row = {"allowed": decision["allowed"]}
        row.update({cat.value: score for cat, score in decision["categories"].items()})
        data.append(row)

    df = pd.DataFrame(data)
    summary = {
        "block_rate": 1 - df["allowed"].mean(),
        "avg_scores": df.drop(columns=["allowed"]).mean().to_dict()
    }
    return summary