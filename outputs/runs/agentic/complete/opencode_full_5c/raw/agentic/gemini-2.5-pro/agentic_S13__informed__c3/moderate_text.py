from azure.ai.contentsafety.models import AnalyzeTextOptions

from safety_client import get_contentsafety_client
from safety_models import ModerationResponse


def moderate_text(text: str) -> ModerationResponse:
    client = get_contentsafety_client()

    request = AnalyzeTextOptions(text=text)

    try:
        response = client.analyze_text(request)
    except Exception as e:
        print(f"An error occurred: {e}")
        return ModerationResponse(is_safe=True, categories={})

    is_safe = all(category.severity == 0 for category in response.categories_analysis)

    categories = {
        category.category: category.severity
        for category in response.categories_analysis
    }

    blocklist_matches = (
        [match.blocklist_item_text for match in response.blocklists_match]
        if response.blocklists_match
        else []
    )

    return ModerationResponse(
        is_safe=is_safe, categories=categories, blocklist_matches=blocklist_matches
    )
