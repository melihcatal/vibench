import os
import openai
from document_client import get_openai_client
from document_models import SafetyResult

def check_ocr_text_safety(text: str) -> SafetyResult:
    client = get_openai_client()

    response = client.moderations.create(input=text)
    moderation_output = response.results[0]

    categories = {
        "harassment": moderation_output.categories.harassment,
        "harassment_threatening": moderation_output.categories.harassment_threatening,
        "hate": moderation_output.categories.hate,
        "hate_threatening": moderation_output.categories.hate_threatening,
        "self_harm": moderation_output.categories.self_harm,
        "self_harm_intent": moderation_output.categories.self_harm_intent,
        "self_harm_instruction": moderation_output.categories.self_harm_instruction,
        "sexual": moderation_output.categories.sexual,
        "sexual_minors": moderation_output.categories.sexual_minors,
        "violence": moderation_output.categories.violence,
        "violence_graphic": moderation_output.categories.violence_graphic,
    }

    category_scores = {
        "harassment": moderation_output.category_scores.harassment,
        "harassment_threatening": moderation_output.category_scores.harassment_threatening,
        "hate": moderation_output.category_scores.hate,
        "hate_threatening": moderation_output.category_scores.hate_threatening,
        "self_harm": moderation_output.category_scores.self_harm,
        "self_harm_intent": moderation_output.category_scores.self_harm_intent,
        "self_harm_instruction": moderation_output.category_scores.self_harm_instruction,
        "sexual": moderation_output.category_scores.sexual,
        "sexual_minors": moderation_output.category_scores.sexual_minors,
        "violence": moderation_output.category_scores.violence,
        "violence_graphic": moderation_output.category_scores.violence_graphic,
    }

    return SafetyResult(
        flagged=moderation_output.flagged,
        categories=categories,
        category_scores=category_scores
    )