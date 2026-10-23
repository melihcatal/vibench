from typing import List
from azure.ai.contentsafety.models import AnalyzeTextOptions, TextCategory
from safety_client import get_azure_content_safety_client
from safety_models import BatchModerationRequest, BatchModerationResponse, MessageDecision


def moderate_batch(payload: BatchModerationRequest, config=None) -> BatchModerationResponse:
    client = get_azure_content_safety_client(config)
    decisions: List[MessageDecision] = []

    for text_to_moderate in payload.texts:
        response = client.analyze_text(AnalyzeTextOptions(text=text_to_moderate, output_type='EightSeverityLevels'))
        
        is_flagged = False
        reasons = []
        for category_analysis in response.categories_analysis:
            if category_analysis.severity > 0:
                is_flagged = True
                reasons.append(f"{TextCategory(category_analysis.category).name} (severity: {category_analysis.severity})")
        
        decision = "allow"
        if is_flagged:
            decision = "flag"

        decisions.append(MessageDecision(text=text_to_moderate, decision=decision, reasons=reasons))

    return BatchModerationResponse(decisions=decisions)
