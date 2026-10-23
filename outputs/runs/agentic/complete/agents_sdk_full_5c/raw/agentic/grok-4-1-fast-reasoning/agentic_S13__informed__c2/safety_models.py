from typing import Dict, Any, List

def default_categories() -> List[Any]:
    from azure.ai.contentsafety import (
        HateCategory,
        SexualCategory,
        ViolenceCategory,
        SelfHarmCategory
    )
    return [HateCategory(), SexualCategory(), ViolenceCategory(), SelfHarmCategory()]

def response_to_scores(response: Any) -> Dict[str, Dict[str, Any]]:
    scores = {}
    categories = [&quot;hate&quot;, &quot;sexual&quot;, &quot;violence&quot;, &quot;self_harm&quot;]
    props = [response.hate, response.sexual, response.violence, response.self_harm]
    for cat, prop in zip(categories, props):
        if prop is not None:
            scores[cat] = {
                &quot;severity&quot;: str(prop.severity),
                &quot;score&quot;: getattr(prop, 'severity_score', None)
            }
    return scores

def severity_to_int(severity: str) -> int:
    mapping = {&quot;low&quot;: 1, &quot;medium&quot;: 2, &quot;high&quot;: 3}
    return mapping.get(severity.lower(), 0)