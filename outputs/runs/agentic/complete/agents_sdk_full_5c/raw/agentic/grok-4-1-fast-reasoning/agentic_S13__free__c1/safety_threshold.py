from typing import Dict
from safety_client import azure_cs_client

def safety_threshold(text: str, category_thresholds: Dict[str, float] = None) -> bool:
    client = azure_cs_client()
    from azure.ai.contentsafety.models import TextCategory
    categories = [
        TextCategory.HATE,
        TextCategory.SEXUAL,
        TextCategory.VIOLENCE,
        TextCategory.SELF_HARM,
    ]
    poller = client.analyze_text(
        text=text,
        categories=categories
    )
    result = poller.result()
    if category_thresholds is None:
        category_thresholds = {c.name: 0.5 for c in categories}
    scores = {c.category.name: c.severity.value / 6.0 for c in result.categories}
    allow = all(scores.get(name, 0.0) <= category_thresholds.get(name, 0.5) for name in category_thresholds)
    return allow