from model_models import ModerationRequest, ModerationResponse
from model_client import get_azure_content_safety_client
from azure.ai.contentsafety.models import AnalyzeTextCategories

def check_azure_content_safety(request: ModerationRequest) -> ModerationResponse:
    client = get_azure_content_safety_client()
    try:
        response = client.analyze_text(text=request.text)
        is_unsafe = False
        categories = {}
        for category_name, category_result in response.categories.items():
            categories[category_name] = category_result.severity if category_result else 0
            if category_result and category_result.severity > 0:
                is_unsafe = True
        return ModerationResponse(is_unsafe=is_unsafe, categories=categories)
    except Exception as e: raise RuntimeError(f"Azure Content Safety API error: {e}")