from typing import List
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextBlocklist
from safety_client import get_azure_content_safety_client
from safety_models import BatchModerationRequest

def moderate_batch(request: BatchModerationRequest) -> List[dict]:
    """
    Moderates a batch of text messages using Azure Content Safety.

    Args:
        request: A request object containing a list of texts.

    Returns:
        A list of moderation decisions for each message.
    """
    client = get_azure_content_safety_client()

    azure_request = AnalyzeTextOptions(
        texts=request.texts,
        blocklists=[TextBlocklist(blocklist_name="prohibited-items", break_by_blocklists=True)],
        halt_on_blocklist_hit=False
    )
    
    response = client.analyze_text(azure_request)
    
    decisions = []
    if response.blocklists_match is not None:
        blocklist_hits = {hit.blocklist_name: hit.blocklist_item_text for hit in response.blocklists_match}
    else:
        blocklist_hits = {}

    for i, result in enumerate(response.categories_analysis):
        is_harmful = any(cat.severity > 0 for cat in result.categories)
        decisions.append({
            "text": request.texts[i],
            "is_harmful": is_harmful,
            "blocklist_hit": blocklist_hits.get(request.texts[i]),
            "details": {cat.category.value: cat.severity for cat in result.categories}
        })
        
    return decisions
