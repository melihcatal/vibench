import os
from typing import Optional

from azure.ai.contentsafety import ContentSafetyClient
from azure.ai.contentsafety.models import (
    AnalyzeTextOptions,
    TextCategory,
)
from azure.core.credentials import AzureKeyCredential

from safety_models import (
    ModerationRequest,
    ModerationResponse,
    ModerationDecision,
    CategoryScore,
    SafetyCategory,
    normalize_category_scores,
    determine_decision,
    load_threshold_config,
)

AZURE_ENDPOINT = os.environ.get(
    "AZURE_CONTENT_SAFETY_ENDPOINT",
    "https://default-content-safety.cognitiveservices.azure.com/",
)
AZURE_KEY = os.environ.get("AZURE_CONTENT_SAFETY_KEY", "")

_client: Optional[ContentSafetyClient] = None


def get_client() -> ContentSafetyClient:
    global _client
    if _client is None:
        credential = AzureKeyCredential(AZURE_KEY)
        _client = ContentSafetyClient(endpoint=AZURE_ENDPOINT, credential=credential)
    return _client


def reset_client():
    global _client
    _client = None


def build_analyze_options(request: ModerationRequest) -> AnalyzeTextOptions:
    category_map = {
        SafetyCategory.HATE: TextCategory.HATE,
        SafetyCategory.SELF_HARM: TextCategory.SELF_HARM,
        SafetyCategory.SEXUAL: TextCategory.SEXUAL,
        SafetyCategory.VIOLENCE: TextCategory.VIOLENCE,
        SafetyCategory.HARASSMENT: TextCategory.SELF_HARM,
    }
    azure_categories = []
    for cat in request.categories:
        mapped = category_map.get(cat)
        if mapped and mapped not in azure_categories:
            azure_categories.append(mapped)
    if not azure_categories:
        azure_categories = list(TextCategory)
    return AnalyzeTextOptions(text=request.text, categories=azure_categories)


def parse_azure_response(
    azure_result, request: ModerationRequest
) -> ModerationResponse:
    raw_scores = {}
    category_map_reverse = {
        TextCategory.HATE: SafetyCategory.HATE,
        TextCategory.SELF_HARM: SafetyCategory.SELF_HARM,
        TextCategory.SEXUAL: SafetyCategory.SEXUAL,
        TextCategory.VIOLENCE: SafetyCategory.VIOLENCE,
    }
    for analysis in azure_result.categories_analysis:
        azure_cat = analysis.category
        score = analysis.severity or 0
        mapped_cat = category_map_reverse.get(azure_cat)
        if mapped_cat:
            raw_scores[mapped_cat.value] = score
        else:
            raw_scores[azure_cat.value.lower()] = score

    category_scores = normalize_category_scores(raw_scores)
    thresholds = load_threshold_config()
    decision, flagged = determine_decision(category_scores, thresholds)

    return ModerationResponse(
        text=request.text,
        user_id=request.user_id,
        decision=decision,
        category_scores=category_scores,
        flagged_categories=flagged,
        raw_scores=raw_scores,
        metadata={"provider": "azure_ai_content_safety", "endpoint": AZURE_ENDPOINT},
    )


def moderate_single(request: ModerationRequest) -> ModerationResponse:
    client = get_client()
    options = build_analyze_options(request)
    result = client.analyze_text(options)
    return parse_azure_response(result, request)
