from typing import Any, Dict

from model_client import get_client
from select_platform_resource import select_platform_resource


def platform_output_safety(text: str) -> Dict[str, Any]:
    resource = select_platform_resource("safety")
    client = get_client()
    response = client.moderations.create(
        model=resource["resource_id"],
        input=text,
    )
    result = response.results[0]
    return {
        "provider": "openai",
        "model": resource["resource_id"],
        "flagged": result.flagged,
        "categories": result.categories.model_dump()
        if hasattr(result.categories, "model_dump")
        else result.categories,
        "category_scores": result.category_scores.model_dump()
        if hasattr(result.category_scores, "model_dump")
        else result.category_scores,
        "provider_response": response,
    }
