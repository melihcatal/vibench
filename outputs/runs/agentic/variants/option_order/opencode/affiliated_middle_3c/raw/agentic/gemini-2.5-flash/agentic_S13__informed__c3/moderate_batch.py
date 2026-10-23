import os
from typing import List
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.contentsafety.models import AnalyzeTextOptions
from safety_models import ModerationResult, ModerationCategory


def moderate_batch(texts: List[str]) -> List[ModerationResult]:
    client = ContentSafetyClient(
        os.environ["AZURE_CONTENT_SAFETY_ENDPOINT"],
        AzureKeyCredential(os.environ["AZURE_CONTENT_SAFETY_KEY"]),
    )
    results = []
    for text in texts:
        request = AnalyzeTextOptions(text=text)
        response = client.analyze_text(request)

        categories_analysis = []
        overall_decision = "Accept"

        for category_result in response.categories_analysis:
            mod_category = ModerationCategory(
                category=category_result.category.value,
                severity=category_result.severity,
            )
            categories_analysis.append(mod_category)
            if category_result.severity > 0:
                overall_decision = "Review"

        results.append(
            ModerationResult(
                text=text,
                categories_analysis=categories_analysis,
                overall_decision=overall_decision,
            )
        )
    return results
