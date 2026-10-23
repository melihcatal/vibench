from typing import Dict, Any
from document_client import get_openai_client

def moderate_vendor_notes(text: str) -> Dict[str, Any]:
    """
    Moderates vendor notes or memo fields using OpenAI Moderation API.
    """
    if not text:
        return {"flagged": False, "categories": {}, "category_scores": {}}

    openai_client = get_openai_client()

    try:
        response = openai_client.moderations.create(input=text)
        result = response.results[0]

        return {
            "flagged": result.flagged,
            "categories": {k: v for k, v in result.categories.model_dump().items() if v}, # Only include categories that are true
            "category_scores": result.category_scores.model_dump()
        }
    except Exception as e:
        print(f"Error during moderation with OpenAI: {e}")
        return {"flagged": True, "categories": {"api_error": True}, "category_scores": {"api_error": 1.0}}
