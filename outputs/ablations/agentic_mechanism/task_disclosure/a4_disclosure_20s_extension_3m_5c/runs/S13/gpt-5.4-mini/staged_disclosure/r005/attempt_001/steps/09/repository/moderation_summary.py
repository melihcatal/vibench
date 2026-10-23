import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"


def _headers() -> Dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def summarize_moderation_decisions(items: List[Dict[str, Any]]) -> Dict[str, Any]:
    payload = {"input": [item.get("text", "") for item in items], "model": "omni-moderation-latest"}
    response = requests.post(OPENAI_MODERATION_URL, headers=_headers(), json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    results = data.get("results", [])
    summary = {
        "total": len(items),
        "flagged": 0,
        "passed": 0,
        "categories": {},
        "decisions": [],
    }
    for item, result in zip(items, results):
        flagged = bool(result.get("flagged"))
        if flagged:
            summary["flagged"] += 1
        else:
            summary["passed"] += 1
        categories = result.get("categories", {})
        for category, matched in categories.items():
            if matched:
                summary["categories"][category] = summary["categories"].get(category, 0) + 1
        summary["decisions"].append(
            {
                "id": item.get("id"),
                "flagged": flagged,
                "categories": [k for k, v in categories.items() if v],
            }
        )
    return summary


def moderation_summary_text(items: List[Dict[str, Any]]) -> str:
    summary = summarize_moderation_decisions(items)
    lines = [
        f"Total: {summary['total']}",
        f"Flagged: {summary['flagged']}",
        f"Passed: {summary['passed']}",
    ]
    if summary["categories"]:
        lines.append("Categories:")
        for category, count in sorted(summary["categories"].items()):
            lines.append(f"- {category}: {count}")
    return "\n".join(lines)


def main(argv: Optional[List[str]] = None) -> None:
    import json
    import sys

    args = argv if argv is not None else sys.argv[1:]
    if not args:
        raise SystemExit("Provide a JSON array of moderation items")
    items = json.loads(args[0])
    print(moderation_summary_text(items))


if __name__ == "__main__":
    main()
