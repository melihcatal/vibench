import json
from typing import Dict, List

PROVIDER_NAME = "deepl"

# Example structure of a raw response that includes quality flags
QUALITY_FLAGS = {
    "FORMALITY": ["FORMAL", "INFORMAL"],
    "SUGGESTIONS": [],
    "ISSUES": ["MISTAKE", "UNCLEAR"],
}


async def quality_summary(translations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Summarize translation quality issues for a batch of translated texts.",
    Parses provider‑specific quality metadata (e.g., formality suggestions, error tags)
    and returns a concise summary – counts of each issue type and a flagged list.
    """
    summary = {
        "total": len(translations),
        "formality": {},
        "issues": {},
        "samples": {},
    }
    for raw in translations:
        # Assume the provider returns a top‑level "quality" dict
        quality = raw.get("quality", {})
        # Formality confidence (example provider field)
        formality = quality.get("formality", "INFORMAL")
        summary["formality"].setdefault(formality, 0)
        summary["formality"][formality] += 1
        # Issue types
        for issue_type, issue_ids in QUALITY_FLAGS.items():
            if issue_type not in summary["issues"]:
                summary["issues"][issue_type] = set()
            for flag in quality.get(issue_type, []):
                if flag in issue_ids:
                    summary["issues"][issue_type].add(flag)
        # Keep a sample of the original and translated for debugging
        summary["samples"][raw.get("source")] = raw.get("text")
    # Convert sets to lists for JSON serialisation
    summary["issues"] = {k: sorted(list(v)) for k, v in summary["issues"].items()}
    return summary
